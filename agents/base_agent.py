import asyncio
import uuid
from typing import Dict, Any, Optional
from core.aether_conductor import conductor
from core.envelope import Envelope, AetherIntent

class BaseAgent:
    def __init__(self, agent_id: str, conductor_ref=conductor):
        self.agent_id = agent_id
        self.bus = conductor_ref
        print(f"🤖 [Agent] '{agent_id}' Connected to Aether.")

    async def subscribe(self, topic: str, handler):
        await self.bus.subscribe(topic, handler)

    async def publish(self, topic: str, intent: AetherIntent, payload: Dict[str, Any], flow_id: str = None):
        env = Envelope(
            intent=intent,
            sender_id=self.agent_id,
            payload=payload,
            flow_id=flow_id or str(uuid.uuid4())
        )
        await self.bus.publish(topic, env)

    async def start(self):
        pass
