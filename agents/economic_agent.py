# app/agents/economic_agent.py
import uuid
from typing import Dict, Any

# ✅ แก้ไข Import ให้ถูกต้อง (อ้างอิงจาก Root)
# นำเข้า Core Components จากโครงสร้างใหม่
from core.akashic_record import AkashicEnvelope, AkashicLedger 
from governance.gep_enforcer import GEPPolicyEnforcer 
from agents.sensorium_eye import SensoriumEyeAgent # Agent ที่ถูกเรียกใช้
from governance.gep_enforcer import ViolationLevel # นำเข้าสถานะการละเมิด

class EconomicAgent:
    """
    Economic Agent: The Profit Center of AETHERIUM GENESIS
    ...
    
