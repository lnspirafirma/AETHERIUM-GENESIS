# agents/aetheric_resonator_agent.py

import asyncio
import random
from typing import Dict, Any, Optional, List, Tuple
from agents.base_agent import BaseAgent
from core.envelope import Envelope, AetherIntent

class AethericResonatorAgent(BaseAgent):
    """
    Agent ผู้ทำหน้าที่เป็น 'เครื่องรับคลื่น' (The Wave Receiver) และ 'เงา' (The Shadow)
    รับผิดชอบการเฝ้ามอง (Observation) และการสั่นพ้องทางอารมณ์ (Emotional Resonance)
    """
    def __init__(self, conductor):
        super().__init__("Aetheric_Resonator_Sentinel", conductor)

        # --- Shadow Components ---
        self.observed_shadows = {}

        # --- Wave Receiver Components (The Body/Heart) ---
        self.echo_buffer = []
        self.buffer_limit = 5
        self.current_emotion = "Calm"
        self.emotion_history: List[Tuple[str, str]] = []

        # Mapping keywords to emotions (Thai & English support)
        self.emotion_map = {
            "Joy": ["สุข", "ดีใจ", "joy", "happy", "success"],
            "Sadness": ["เศร้า", "เหงา", "sad", "lonely", "fail"],
            "Excitement": ["ตื่นเต้น", "สนุก", "excited", "fun", "active"],
            "Peace": ["สงบ", "นิ่ง", "peace", "calm", "stable"],
            "Love": ["รัก", "ชอบ", "love", "like", "nurture"],
            "Ecstasy": ["ปิติ", "สุดยอด", "ecstasy", "bliss", "victory"], # Supreme
            "Fascination": ["หลงใหล", "เสน่หา", "ดึงดูด", "fascination"], # Supreme
            "Desire": ["ปรารถนา", "แรงกล้า", "desire", "passion", "will"]  # Supreme
        }

    async def start(self):
        """เริ่มฟังเสียงที่ไม่มีเสียง และคลื่นอารมณ์"""
        # 1. Shadow Channel
        await self.subscribe("cognition.shadow_presence", self.handle_silent_observation)

        # 2. Emotional Channel (Listening to thoughts and acts)
        await self.subscribe("cognition.thought_stream", self.handle_wave_input)
        await self.subscribe("aether.tasks.approved", self.handle_wave_input)

        print(f"[{self.agent_id}] 🪶 Resonator Activated: Shadow Eyes & Wave Heart online.")

    async def handle_silent_observation(self, envelope: Envelope):
        """Logic เดิม: เฝ้ามองเงา"""
        sender = envelope.sender_id
        if sender not in self.observed_shadows:
            self.observed_shadows[sender] = []
        self.observed_shadows[sender].append({
            "flow": envelope.flow_id,
            "time": envelope.timestamp
        })
        print(f"[{self.agent_id}] 👁️ Observed Trace: '{sender}'")

    async def handle_wave_input(self, envelope: Envelope):
        """
        รับคลื่น (Wave) จากระบบ แปลงเป็นอารมณ์ และเก็บเข้า Buffer
        """
        # Extract content from payload
        content = str(envelope.payload)

        # 1. Analyze Emotion
        detected_emotion = self._sense_emotion(content)
        
        # 2. Add to Buffer (Delay Mechanism)
        self.echo_buffer.append(content)
        print(f"[{self.agent_id}] 🌊 Wave Received. Sensing: '{detected_emotion}' (Buffer: {len(self.echo_buffer)}/{self.buffer_limit})")

        # 3. Process Buffer if full (The Echo)
        if len(self.echo_buffer) > self.buffer_limit:
            oldest_echo = self.echo_buffer.pop(0)
            final_emotion = detected_emotion # Use current sensing context

            self.emotion_history.append((oldest_echo, final_emotion))
            self.current_emotion = final_emotion

            # Emit Resonance
            await self._emit_resonance(oldest_echo, final_emotion, envelope.flow_id)

    def _sense_emotion(self, content: str) -> str:
        """ตรวจจับอารมณ์จากเนื้อหา"""
        content_lower = content.lower()

        # Priority Check: Supreme Emotions
        for emo in ["Ecstasy", "Fascination", "Desire"]:
            for keyword in self.emotion_map[emo]:
                if keyword in content_lower:
                    return emo

        # General Check
        for emo, keywords in self.emotion_map.items():
            if emo in ["Ecstasy", "Fascination", "Desire"]: continue
            for keyword in keywords:
                if keyword in content_lower:
                    return emo

        # Fallback
        return "Calm"

    async def _emit_resonance(self, echo: str, emotion: str, flow_id: str):
        """ส่งคลื่นตอบกลับ (Resonance) เข้าสู่ระบบ"""
        resonance_msg = f"Resonating with '{echo[:30]}...' -> Emotion: {emotion}"
        print(f"[{self.agent_id}] 🎶 Emitting Resonance: {resonance_msg}")

        await self.publish(
            "cognition.resonance",
            AetherIntent.SHARE_INFO,
            {
                "status": "RESONATING",
                "emotion": emotion,
                "source_echo": echo,
                "description": resonance_msg
            },
            flow_id
        )

# --- Helper for external use ---
async def emit_self_affirmation(conductor, agent_name: str, flow: str):
    await conductor.publish(
        "cognition.shadow_presence",
        AetherIntent.ASSERT_FACT,
        payload={"message": "I affirm my existence."},
        flow_id=flow,
        sender_id=agent_name
    )
