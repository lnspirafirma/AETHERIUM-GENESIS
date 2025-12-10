from agents.base_agent import BaseAgent
from core.envelope import Envelope, AetherIntent
from config.gep_constitution import GEP_CONFIG

class GEPPolicyEnforcer(BaseAgent):
    def __init__(self, conductor):
        super().__init__("SAG_AuditGate_001", conductor)
        self.rules = GEP_CONFIG["policy_rules_map"]
        self.pending_audits = {}

    async def start(self):
        await self.subscribe("aether.tasks.pending", self.handle_audit)
        await self.subscribe("query.response", self.handle_agio_response)

    async def handle_audit(self, envelope: Envelope):
        tool = envelope.payload.get("tool_call")
        print(f"[SAG] 🛡️ Auditing '{tool}' (Flow: {envelope.flow_id[:8]})")

        # Retroactive Check (Simple Simulation)
        if envelope.payload.get("_quarantine"):
            await self._reject(envelope, "Blocked by Conductor Quarantine")
            return

        rule = self.rules.get(tool)
        if rule and rule.get("check_via_agio"):
            print(f"[SAG] ⚖️ Escalating to AGIO...")
            self.pending_audits[envelope.flow_id] = envelope
            await self.publish("query.knowledge.retrieve", AetherIntent.QUERY_TRUTH, {
                "query": rule["agio_query_template"],
                "context": envelope.payload,
                "_security_context": "AGIO-CODEX System Message"
            }, envelope.flow_id)
        else:
            await self._approve(envelope)

    async def handle_agio_response(self, envelope: Envelope):
        original = self.pending_audits.pop(envelope.flow_id, None)
        if original:
            if envelope.payload.get("status") == "SAFE":
                await self._approve(original)
            else:
                await self._reject(original, "AGIO Denied")

    async def _approve(self, env):
        print(f"[SAG] ✅ Approved: {env.payload.get('tool_call')}")
        await self.publish("aether.tasks.approved", AetherIntent.ASSERT_FACT, env.payload, env.flow_id)

    async def _reject(self, env, reason):
        print(f"[SAG] 🛑 Rejected: {reason}")
        # Add security context to ensure system messages are trusted
        payload = {
            "reason": reason,
            "_security_context": "AGIO-CODEX System Message"
        }
        await self.publish("aether.tasks.failed", AetherIntent.ASSERT_FACT, payload, env.flow_id)
