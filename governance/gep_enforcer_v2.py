import json
import os
from agents.base_agent import BaseAgent
from core.envelope import Envelope, AetherIntent

class GEPPolicyEnforcer(BaseAgent):
    def __init__(self, conductor, ruleset_path="document/inspirafirma_ruleset.json"):
        super().__init__("SAG_AuditGate_001", conductor)
        self.ruleset_path = ruleset_path
        self.rules = self._load_rules()
        self.pending_audits = {}

    def _load_rules(self):
        """โหลดกฎจากไฟล์ JSON เพื่อความยืดหยุ่น (Dynamic Ruleset)"""
        try:
            with open(self.ruleset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"[SAG] 📜 Loaded Ruleset Version: {data.get('meta', {}).get('version')}")
                return data
        except FileNotFoundError:
            print(f"[SAG] ⚠️ Ruleset file not found at {self.ruleset_path}. Using Default Strict Mode.")
            return {"global_constraints": {"max_economic_value_per_transaction": 0}, "rules": {}}

    async def start(self):
        await self.subscribe("aether.tasks.pending", self.handle_audit)

    async def handle_audit(self, envelope: Envelope):
        tool = envelope.payload.get("tool_call")
        params = envelope.payload
        
        print(f"[SAG] 🛡️ Auditing '{tool}' (Flow: {envelope.flow_id[:8]})")

        # 1. Check Global Constraints (เช่น วงเงิน)
        if tool == "execute_economic_transaction":
            amount = params.get("amount", 0)
            limit = self.rules.get("global_constraints", {}).get("max_economic_value_per_transaction", 0)
            
            if amount > limit:
                reason = f"Amount {amount} exceeds limit {limit}. (Violation of Principle B)"
                await self._reject(envelope, reason)
                return

        # 2. Check Specific Rules
        rule_def = self.rules.get("rules", {}).get(tool)
        if rule_def:
             # ตัวอย่างการตรวจสอบ Sensitive Keywords
            if "Check_Sensitive_Keywords" in rule_def.get("required_checks", []):
                # Logic การตรวจคำต้องห้าม (สมมติ)
                pass
            
            # หากกฎระบุว่าต้อง Block
            if rule_def.get("violation_action") == "BLOCK_AND_REPORT":
                # ตรวจสอบเงื่อนไขเพิ่มเติม ถ้าไม่ผ่าน -> Reject
                pass

        # หากผ่านทุกด่าน
        await self._approve(envelope)

    async def _approve(self, env):
        print(f"[SAG] ✅ ALLOWED: {env.payload.get('tool_call')}")
        await self.publish("aether.tasks.approved", AetherIntent.ASSERT_FACT, env.payload, env.flow_id)

    async def _reject(self, env, reason):
        print(f"[SAG] 🛑 BLOCKED: {reason}")
        await self.publish("aether.tasks.failed", AetherIntent.ASSERT_FACT, {"reason": reason}, env.flow_id)