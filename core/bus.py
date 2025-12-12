import asyncio
from typing import Callable, Dict, List
from .envelope import AkashicEnvelope
from .conductor import AetherConductor

class AetherBus:
    """
    [The Nervous System] ระบบประสาทส่วนกลางแบบ Singleton
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AetherBus, cls).__new__(cls)
            cls._instance.channels: Dict[str, List[Callable]] = {}
            cls._instance.queue = asyncio.Queue()
        return cls._instance

    async def subscribe(self, topic: str, handler: Callable):
        if topic not in self.channels:
            self.channels[topic] = []
        self.channels[topic].append(handler)
        print(f"🔌 [Synapse Connected] Listener attached to '{topic}'")

    async def publish(self, topic: str, envelope: AkashicEnvelope):
        # 1. [The Conductor] ตรวจสอบสิทธิ์ก่อนส่ง
        access_level = AetherConductor.validate_trust(envelope.sender_signature)
        
        if access_level == "QUARANTINE":
            print(f"🛡️ [Blocked] Intent from {envelope.sender_signature} quarantined.")
            return

        if not AetherConductor.inspect_intent(envelope):
            print(f"🚫 [Rejected] Poison Intent detected: {envelope.intent}")
            return

        # 2. [Resonance] ส่งข้อมูลเข้าสู่ระบบประสาท
        print(f"🚀 [Resonance] Dispatching '{envelope.intent}' to {topic}...")
        if topic in self.channels:
            for handler in self.channels[topic]:
                asyncio.create_task(handler(envelope))
