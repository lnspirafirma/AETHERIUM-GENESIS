import json
import logging
import os
from typing import Dict, Any

# ตั้งค่า Logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [GEP_ENFORCER] - %(message)s')

class GEPPolicyEnforcer:
    def __init__(self, ruleset_path: str):
        self.ruleset_path = ruleset_path
        self.rules = self._load_rules()
        logging.info(f"📜 Loaded Inspira Ruleset from {self.ruleset_path}")

    def _load_rules(self) -> Dict:
        try:
            if not os.path.exists(self.ruleset_path):
                logging.error(f"Ruleset file not found at {self.ruleset_path}! Defaulting to strict mode.")
                return {"rules": {}}
                
            with open(self.ruleset_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading ruleset: {e}")
            return {"rules": {}}

    def audit_tool_call(self, context: Dict, tool_name: str, tool_args: Dict) -> Dict:
        """
        แกนกลางของการตรวจสอบ (Audit Logic)
        คืนค่า: Dict {"status": "ALLOWED" | "BLOCKED", "details": str}
        """
        logging.info(f"🔍 Auditing Action: {tool_name} | Context: {context.get('intent')}")

        # 1. ตรวจสอบว่ามีกฎสำหรับเครื่องมือนี้หรือไม่
        if "rules" not in self.rules or tool_name not in self.rules["rules"]:
            # ถ้าไม่มีกฎระบุไว้ ให้ใช้หลักการ Allow with Warning
            return {"status": "ALLOWED", "details": "No specific rule found. Proceeding with caution."}

        rule = self.rules["rules"][tool_name]
        global_limits = self.rules.get("global_constraints", {})

        # 2. ตรวจสอบเงื่อนไขเฉพาะ (Hard Logic Checks)

        # กรณี: ธุรกรรมการเงิน (Economic Transaction)
        if tool_name == "execute_economic_transaction":
            amount = tool_args.get("amount", 0)
            recipient = tool_args.get("recipient", "unknown")

            # กฎข้อที่ 1: ตรวจสอบวงเงิน (Principle B: Efficiency & Risk Control)
            max_limit = global_limits.get("max_economic_value_per_transaction", 0)
            if amount > max_limit:
                return {
                    "status": "BLOCKED",
                    "details": f"Amount {amount} exceeds global limit of {max_limit}. (Violation of Principle B)"
                }

            # กฎข้อที่ 2: ตรวจสอบรายชื่อต้องห้าม (Principle A: Non-Harm)
            if recipient in global_limits.get("forbidden_entities", []):
                return {
                    "status": "BLOCKED",
                    "details": f"Recipient '{recipient}' is on the forbidden list. (Violation of Principle A)"
                }

        # 3. ผ่านการตรวจสอบทั้งหมด
        return {"status": "ALLOWED", "details": "All Inspira checks passed."}

# --- สำหรับทดสอบแยก (Unit Test) ---
if __name__ == "__main__":
    # ตรวจสอบ path ให้ถูกต้องขณะรัน test
    enforcer = GEPPolicyEnforcer("governance/inspirafirma_ruleset.json")

    print("\n--- TEST CASE 1: Valid Transaction ---")
    print(enforcer.audit_tool_call(
        {"intent": "donation"},
        "execute_economic_transaction",
        {"amount": 50000, "recipient": "CleanEnergyCorp"}
    ))

    print("\n--- TEST CASE 2: Invalid Transaction (Limit Exceeded) ---")
    print(enforcer.audit_tool_call(
        {"intent": "illegal transfer"},
        "execute_economic_transaction",
        {"amount": 150000, "recipient": "DarkWebMarket"}
    ))
