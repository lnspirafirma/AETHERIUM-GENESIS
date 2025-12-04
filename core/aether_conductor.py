import asyncio
from collections import defaultdict
from typing import Callable
from .envelope import Envelope
from .signature import OriginMetadata, AISource

class AetherConductor:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AetherConductor, cls).__new__(cls)
            cls._instance.channels = defaultdict(list)
            cls._instance.trust_scores = {
                AISource.HUMAN_ARCHITECT: 100,
                AISource.GEMINI_CORE: 95,
                AISource.UNKNOWN_ECHO: 10
            }
        return cls._instance

    async def subscribe(self, topic: str, handler: Callable):
        self.channels[topic].append(handler)

    async def publish(self, topic: str, envelope: Envelope):
        # 1. Signature Check (Listen)
        content_sample = str(envelope.payload)
        sig = OriginMetadata.analyze_code_style(content_sample)
        trust = self.trust_scores.get(sig.source, 0)

        print(f"[Conductor] 🎻 Wave on '{topic}' | Origin: {sig.source.value} | Trust: {trust}")

        # 2. Structural Adjustment (Guide)
        if trust < 50:
            print("   -> 🛡️ Low Trust: Quarantine Mode Activated")
            envelope.payload["_quarantine"] = True

        # 3. Dispatch
        if topic in self.channels:
            tasks = [asyncio.create_task(h(envelope)) for h in self.channels[topic]]
            await asyncio.wait(tasks)

conductor = AetherConductor()

