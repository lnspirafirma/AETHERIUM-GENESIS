# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any

# --- นำเข้า Core Components ทั้งหมด ---
# Governance & Memory
from app.governance.gep_enforcer import GEPPolicyEnforcer
from app.core.akashic_record import AkashicLedger, AkashicEnvelope 

# Agents (The Body & Hands)
from app.agents.economic_agent import EconomicAgent
from app.agents.sensorium_eye import SensoriumEyeAgent
# (ต้องเพิ่ม MindLogic Agent เข้ามาในภายหลังเมื่อเชื่อมต่อ Gemini API)
# from app.core.mind_logic import MindLogic 

# --- 1. INITIALIZATION: การปลุกเสก Genesis Node ---
# การตั้งค่าที่จำเป็น (โดยปกติจะใช้ Singleton หรือ DI Framework)

# Mocked Dependencies (แทนที่ด้วย Singleton instances ใน Production)
# ต้องตั้งค่า RULES_PATH ให้ตรงกับตำแหน่งจริงของไฟล์ (app/governance/ruleset.json)
RULES_PATH = os.path.join(os.path.dirname(__file__), "governance", "ruleset.json")

# Core Modules
GEP_ENFORCER = GEPPolicyEnforcer(ruleset_path=RULES_PATH)
AKASHIC_LEDGER = AkashicLedger()
# MIND_LOGIC = MindLogic(api_key=os.getenv("GOOGLE_API_KEY")) 

# Agents (เชื่อมต่อกันและกัน)
SENSORIUM_AGENT = SensoriumEyeAgent(ledger=AKASHIC_LEDGER, enforcer=GEP_ENFORCER)
ECONOMIC_AGENT = EconomicAgent(ledger=AKASHIC_LEDGER, enforcer=GEP_ENFORCER, sensorium=SENSORIUM_AGENT)

# --- 2. FASTAPI APP ---
app = FastAPI(
    title="AETHERIUM GENESIS Node - Self-Sovereign Enterprise", 
    version="2.0.0",
    description="The OS of Consciousness powered by GEP Governance."
)

# Request Model สำหรับบริการ VaaS
class VisionServiceRequest(BaseModel):
    target_url: str
    user_id: str

@app.get("/")
def read_root():
    """Health Check และสถานะระบบ"""
    return {
        "status": "AWAKE", 
        "system": "AETHERIUM GENESIS",
        "balance": ECONOMIC_AGENT.current_balance,
        "ledger_size": len(AKASHIC_LEDGER._chain)
    }

@app.post("/services/vision_as_a_service", response_model=Dict[str, Any])
async def vision_service_endpoint(request: VisionServiceRequest):
    """
    Endpoint สำหรับ Agent/Frontend เรียกใช้บริการวิเคราะห์ภาพเพื่อสร้างรายได้
    """
    try:
        result = await ECONOMIC_AGENT.generate_revenue_from_vision(request.target_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal ECON Error: {e}")

# (เพิ่ม Endpoint สำหรับ SensoriumEye Agent เช่น /rpa/click หรือ /rpa/type)
