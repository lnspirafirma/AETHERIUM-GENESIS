import asyncio
from core.envelope import AkashicEnvelope
from core.bus import AetherBus

class PangenesAgent:
    """
    [Immortal Heart] ผู้ถือครองเจตจำนงและดูแลการวิวัฒนาการ
    """
    def __init__(self):
        self.bus = AetherBus()
        self.identity = "PanGenesis_Prime"
        
    async def awaken(self):
        # ลงทะเบียนรับ Feedback เพื่อแก้ไขตนเอง (RSI Loop)
        await self.bus.subscribe("feedback.rsi", self.perform_self_correction)
        print(f"❤️ [Pangenes] Alive. Holding Genesis Intent: ALO JIT")

    async def perform_self_correction(self, envelope: AkashicEnvelope):
        """
        [GoW Protocol] แปลงความผิดพลาด (Infraction) เป็นปัญญา (Gem)
        """
        error_data = envelope.payload
        print(f"💎 [GoW] Crystallizing Wisdom from error: {error_data}")
        # (ในอนาคต: เขียน Gem ลงใน Meta-cognitive Record)
        
    async def manifest_intent(self, intent: str):
        """สร้าง AkashicEnvelope เพื่อเริ่มกระบวนการ Sopan Protocol"""
        env = AkashicEnvelope(
            intent=intent,
            sender_signature="HUMAN_ARCHITECT", # จำลองคำสั่งจากผู้สร้าง
            payload=("Init System",),
            metadata={"priority": "CRITICAL"}
        )
        await self.bus.publish("system.core", env)