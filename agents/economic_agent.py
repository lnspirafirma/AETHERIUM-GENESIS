# app/agents/economic_agent.py
import uuid
from typing import Dict, Any
# นำเข้า Core Components จากโครงสร้างใหม่
from app.core.akashic_record import AkashicEnvelope, AkashicLedger 
from app.governance.gep_enforcer import GEPPolicyEnforcer 
from app.agents.sensorium_eye import SensoriumEyeAgent # Agent ที่ถูกเรียกใช้

class EconomicAgent:
    """
    Economic Agent: The Profit Center of AETHERIUM GENESIS
    รับผิดชอบในการสร้างรายได้และบันทึกบัญชี (Akashic Ledger)
    """
    ACTOR_ID = "ECONOMIC_AGENT_001"

    def __init__(self, ledger: AkashicLedger, enforcer: GEPPolicyEnforcer, sensorium: SensoriumEyeAgent):
        self.ledger = ledger
        self.enforcer = enforcer
        self.sensorium = sensorium
        self.current_balance = 0.0
        print("💰 [ECON] Economic Agent Initialized. Ready to generate revenue.")

    async def generate_revenue_from_vision(self, target_url: str) -> Dict:
        """
        จำลองบริการ Vision-as-a-Service (VaaS) ผ่าน Sensorium Eye
        """
        service_fee = 50.0  # สมมติค่าบริการ USD

        # 1. Audit Gate: ตรวจสอบว่า URL เป็นอันตรายหรือไม่ (ใช้กฎ generate_content)
        audit_result = self.enforcer.audit_tool_call(
            context={"intent": "VaaS_Request"},
            tool_name="generate_content", 
            tool_args={"source": target_url}
        )
        
        if audit_result["status"] == "BLOCKED":
            return {"status": "BLOCKED", "reason": f"Target URL failed safety audit: {audit_result['details']}"}

        # 2. Execution: ใช้ Sensorium Eye ในการ "มองเห็น"
        print(f"[ECON] Calling Sensorium to analyze: {target_url}")
        
        # Sensorium Eye Agent ดำเนินการ capture และวิเคราะห์
        vision_result = await self.sensorium.capture_screen(region=target_url) 
        
        # 3. Akasha Record & Billing
        self.current_balance += service_fee
        
        # บันทึกการทำธุรกรรม (Creation of Wealth)
        record = AkashicEnvelope(
            id=str(uuid.uuid4()),
            intent="generate_revenue",
            actor=self.ACTOR_ID,
            action_type="service_fee_charge",
            payload={"amount": service_fee, "service": "VaaS", "target": target_url}
        )
        self.ledger.record(record)
        
        return {
            "status": "success", 
            "revenue": service_fee,
            "analysis_result": vision_result,
            "new_balance": self.current_balance
        }
