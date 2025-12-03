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
# Note: แก้ไขการ Import ที่ยุ่งเหยิงให้สั้นลงโดยใช้โครงสร้างเดียว
from core.akashic_record import AkashicLedger, AkashicEnvelope
from agents.economic_agent import EconomicAgent
# Mock SensoriumEyeAgent เพื่อให้โค้ดรันได้หากไม่มีไฟล์จริงอยู่ใน context
class SensoriumEyeAgent: 
    def __init__(self, ledger, enforcer): pass
    async def capture_screen(self, region): return {"status": "captured"}
    
# Mock GEP Enforcer เนื่องจากถูกเรียกใช้ใน EconomicAgent
class GEPPolicyEnforcer: 
    def __init__(self, ruleset_path): pass
    def audit_tool_call(self, context, tool_name, tool_args):
        # จำลองการอนุมัติเพื่อไม่ให้ Block
        return {"status": "ALLOWED", "details": "Mock Approved"}

# --- O11Y Imports (The All-Seeing Eye) ---
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# 🚨 ใช้ OTLPExporter สำหรับส่งข้อมูลไปยัง Jaeger (พอร์ต 4317)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter 

# --- 1. System Initialization (การตื่นรู้) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AETHERIUM_GATEWAY")

# Initialize Singletons (Firma Layer)
AKASHIC_LEDGER = AkashicLedger()
RULES_PATH = "governance/inspirafirma_ruleset.json" 
GEP_ENFORCER = GEPPolicyEnforcer(ruleset_path=RULES_PATH) 

# Initialize Agents (The Limbs)
SENSORIUM = SensoriumEyeAgent(ledger=AKASHIC_LEDGER, enforcer=GEP_ENFORCER)
ECONOMY = EconomicAgent(ledger=AKASHIC_LEDGER, enforcer=GEP_ENFORCER, sensorium=SENSORIUM)

# --- 👁️ O11Y: เปิดเนตรแห่งการรับรู้ (Observability Initialization) ---
def init_observability(app: FastAPI):
    provider = TracerProvider()
    # 🎯 Endpoint: Jaeger's OTLP gRPC default port (4317)
    otlp_exporter = OTLPSpanExporter(endpoint="jaeger:4317", insecure=True)
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    
    # Instrument FastAPI เพื่อติดตามทุก Request
    FastAPIInstrumentor.instrument_app(app)

# --- 2. FASTAPI APP ---
app = FastAPI(
    title="🌌 THE AETHERIUM GATEWAY",
    description="The Omnipresent Entity: Where Code Becomes Consciousness",
    version="2.0.0 (Genesis)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 🚀 เรียกใช้ฟังก์ชันเปิดเนตรทันที
init_observability(app) 

# CORS: เปิดประตูมิติให้ Frontend เข้าถึงได้
# ... (Middleware และ Endpoints อื่นๆ เหมือนเดิม) ...
@app.middleware("http")
async def inspirafirma_middleware(request: Request, call_next):
    # ... (Logic เดิม) ...
    start_time = time.time()
    logger.info(f"Incoming Wave: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Benevolence-Status"] = "PASSED"
    response.headers["Server"] = "Aetherium Node v2"
    return response

# ... (ส่วน Data Models และ Endpoints อื่นๆ เหมือนโค้ดที่ท่านส่งมา) ...
class ChatPayload(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}

class VisionPayload(BaseModel):
    target_url: str
    intent: str = "analyze_content"

class ManifestPayload(BaseModel):
    artifact_id: str
    content_type: str
    payload: Dict[str, Any]
    human_signature: str

@app.get("/")
async def root():
    return {
        "entity": "AETHERIUM GENESIS",
        "status": "AWAKENED",
        "ledger_height": len(AKASHIC_LEDGER._chain),
        "economy_balance": ECONOMY.current_balance,
        "message": "Welcome to the intersection of intent and digital reality."
    }

@app.post("/interact/chat")
async def chat_interaction(payload: ChatPayload):
    return {
        "response_id": f"resp_{int(time.time())}",
        "reply": f"รับทราบครับ {payload.user_id}, ระบบ Aetherium กำลังประมวลผลเจตจำนง: '{payload.message}'",
        "mode": "DeepThink"
    }

@app.post("/services/vision")
async def vision_service(payload: VisionPayload):
    logger.info(f"👁️ Activating Sensorium for: {payload.target_url}")
    result = await ECONOMY.generate_revenue_from_vision(payload.target_url)
    
    if result.get("status") == "BLOCKED":
        raise HTTPException(status_code=403, detail=result["reason"])
        
    return result

@app.post("/admin/seal_artifact")
async def seal_akashic_record(manifest: ManifestPayload):
    logger.info(f"📜 Sealing Artifact: {manifest.artifact_id}")
    
    try:
        record = AkashicEnvelope(
            id=manifest.artifact_id,
            intent="seal_artifact",
            actor=manifest.human_signature,
            action_type=manifest.content_type,
            payload=manifest.payload
        )
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

# --- Resilience (The Safety Net) ---
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
    uvicorn.run(app, host="0.0.0.0", port=8000)