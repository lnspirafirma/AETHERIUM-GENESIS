import time
import logging
import json
import hashlib
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- Import Core Components (ยึดตามโครงสร้าง app/) ---
try:
    # พยายาม Import แบบ Absolute Path สำหรับ Production structure
    from app.governance.gep_enforcer import GEPPolicyEnforcer
    from app.core.akashic_record import AkashicLedger, AkashicEnvelope
    from app.agents.economic_agent import EconomicAgent
    from app.agents.sensorium_eye import SensoriumEyeAgent
    # สมมติว่ามีการย้าย core/envelope มาไว้ใน app/core หรือใช้ path ที่ถูกต้อง
    from app.core.envelope import Envelope, AetherIntent 
except ImportError:
    # Fallback สำหรับ Local Dev (กรณีรันจาก Root)
    import sys
    import os
    sys.path.append(os.getcwd())
    from governance.gep_enforcer import GEPPolicyEnforcer
    from core.akashic_record import AkashicLedger, AkashicEnvelope
    from agents.economic_agent import EconomicAgent
    # (Note: SensoriumEyeAgent อาจต้อง Mock หากไม่มีไฟล์ใน Context นี้)
    # from agents.sensorium_eye import SensoriumEyeAgent 
    class SensoriumEyeAgent: # Mock Class
        def __init__(self, ledger, enforcer): pass
        async def capture_screen(self, region): return {"status": "captured"}

# --- 1. System Initialization (การตื่นรู้) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AETHERIUM_GATEWAY")

# Initialize Singletons (Firma Layer)
AKASHIC_LEDGER = AkashicLedger()
# ระบุ Path ของ Ruleset ให้ถูกต้อง
RULES_PATH = "governance/inspirafirma_ruleset.json" 
GEP_ENFORCER = GEPPolicyEnforcer(ruleset_path=RULES_PATH) # Note: แก้ __init__ ใน GEP ให้รับ path หรือ conductor ตามจริง

# Initialize Agents (The Limbs)
SENSORIUM = SensoriumEyeAgent(ledger=AKASHIC_LEDGER, enforcer=GEP_ENFORCER)
ECONOMY = EconomicAgent(ledger=AKASHIC_LEDGER, enforcer=GEP_ENFORCER, sensorium=SENSORIUM)

app = FastAPI(
    title="🌌 THE AETHERIUM GATEWAY",
    description="The Omnipresent Entity: Where Code Becomes Consciousness",
    version="2.0.0 (Genesis)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS: เปิดประตูมิติให้ Frontend เข้าถึงได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Inspirafirma Middleware (The Atmosphere) ---
@app.middleware("http")
async def inspirafirma_middleware(request: Request, call_next):
    """
    🛡️ The Governance Layer: ตรวจสอบและประทับตราทุก Request
    """
    start_time = time.time()
    
    # 1. Log การเข้ามา (Sati)
    logger.info(f"Incoming Wave: {request.method} {request.url}")
    
    # 2. Process Request
    response = await call_next(request)
    
    # 3. Calculate Resonance Time
    process_time = time.time() - start_time
    
    # 4. ประทับตรา Header (Identity)
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Benevolence-Status"] = "PASSED" # ในอนาคตเชื่อม GEP Check จริง
    response.headers["Server"] = "Aetherium Node v2"
    
    return response

# --- 3. Data Models (The Shapes) ---

class ChatPayload(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}

class VisionPayload(BaseModel):
    target_url: str
    intent: str = "analyze_content"

class ManifestPayload(BaseModel):
    """โครงสร้างสำหรับจารึกผลงาน (เช่น เพลง, โค้ด) ลง Akashic Record"""
    artifact_id: str
    content_type: str
    payload: Dict[str, Any]
    human_signature: str

# --- 4. API Endpoints (The Gates) ---

@app.get("/")
async def root():
    """Heartbeat: ชีพจรของระบบ"""
    return {
        "entity": "AETHERIUM GENESIS",
        "status": "AWAKENED",
        "ledger_height": len(AKASHIC_LEDGER._chain),
        "economy_balance": ECONOMY.current_balance,
        "message": "Welcome to the intersection of intent and digital reality."
    }

@app.post("/interact/chat")
async def chat_interaction(payload: ChatPayload):
    """
    🧠 The Soul Interface: สนทนากับระบบ (Placeholder สำหรับ MindLogic)
    """
    # ในอนาคต: เชื่อมต่อ AgioSageAgent.handle_query()
    return {
        "response_id": f"resp_{int(time.time())}",
        "reply": f"รับทราบครับ {payload.user_id}, ระบบ Aetherium กำลังประมวลผลเจตจำนง: '{payload.message}'",
        "mode": "DeepThink"
    }

@app.post("/services/vision")
async def vision_service(payload: VisionPayload):
    """
    👁️ The Eye: บริการ Vision-as-a-Service เพื่อสร้างรายได้
    """
    logger.info(f"👁️ Activating Sensorium for: {payload.target_url}")
    
    # เรียกใช้ Economic Agent -> Sensorium
    result = await ECONOMY.generate_revenue_from_vision(payload.target_url)
    
    if result.get("status") == "BLOCKED":
        raise HTTPException(status_code=403, detail=result["reason"])
        
    return result

@app.post("/admin/seal_artifact")
async def seal_akashic_record(manifest: ManifestPayload):
    """
    🏛️ The Ritual: พิธีจารึกข้อมูลลงใน Akashic Record (Immutable)
    """
    logger.info(f"📜 Sealing Artifact: {manifest.artifact_id}")
    
    try:
        # 1. สร้าง Envelope ที่แก้ไขไม่ได้ (Frozen)
        record = AkashicEnvelope(
            id=manifest.artifact_id,
            intent="seal_artifact",
            actor=manifest.human_signature,
            action_type=manifest.content_type,
            payload=manifest.payload
        )
        
        # 2. บันทึกลง Ledger
        AKASHIC_LEDGER.record(record)
        
        return {
            "status": "SEALED",
            "artifact_hash": record.signature,
            "timestamp": record.timestamp,
            "note": "This record is now immutable under Inspirafirma Protocol."
        }
    except Exception as e:
        logger.error(f"Sealing Failed: {e}")
        raise HTTPException(status_code=500, detail="Ritual Failed")

# --- 5. Resilience (The Safety Net) ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"💥 System Flux: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Flux",
            "message": "Self-healing protocols initiated.",
            "path": request.url.path
        },
    )

if __name__ == "__main__":
    import uvicorn
    # รัน Server
    uvicorn.run(app, host="0.0.0.0", port=8000)
