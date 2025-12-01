from agents.base_agent import BaseAgent
from core.envelope import Envelope

class ResourceAgent(BaseAgent):
    def __init__(self, conductor):
        super().__init__("ResourceAgent_001", conductor)

    async def start(self):
        await self.subscribe("aether.tasks.approved", self.execute)

    async def execute(self, envelope: Envelope):
        print(f"[Resource] ⚙️ Executing: {envelope.payload.get('tool_call')}")
