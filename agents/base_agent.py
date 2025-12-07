import asyncio
import uuid
import logging
from typing import Dict, Any, Optional, Callable, Awaitable

# สมมติว่ามีการ import จาก module ของโปรเจกต์ (ตามโค้ดเดิมของคุณ)
from core.aether_conductor import conductor
from core.envelope import Envelope, AetherIntent

# ตั้งค่า Logging พื้นฐาน (ปรับแต่งได้ตามต้องการ)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("AetherAgent")

class BaseAgent:
    """
    คลาสแม่แบบสำหรับ Agent ในระบบ AETHERIUM-GENESIS
    จัดการการเชื่อมต่อ รับ-ส่ง ข้อมูลผ่าน Conductor
    """
    def __init__(self, agent_id: str, conductor_ref=conductor):
        self.agent_id = agent_id
        self.bus = conductor_ref
        logger.info(f"🤖 [Agent: {self.agent_id}] Initialized and connected to Aether.")

    async def subscribe(self, topic: str, handler: Callable[[Envelope], Awaitable[None]]):
        """
        ลงทะเบียนรับข้อมูลจาก Topic ที่กำหนด
        """
        logger.info(f"S [Agent: {self.agent_id}] Subscribing to topic: '{topic}'")
        try:
            await self.bus.subscribe(topic, handler)
        except Exception as e:
            logger.error(f"❌ [Agent: {self.agent_id}] Failed to subscribe to '{topic}': {e}")
            raise e

    async def publish(self, topic: str, intent: AetherIntent, payload: Dict[str, Any], flow_id: Optional[str] = None):
        """
        ส่งข้อมูล (Envelope) ไปยัง Topic ที่กำหนด
        """
        # สร้าง Flow ID ใหม่ถ้าไม่มีการระบุมา (สำหรับการ Trace การทำงานข้าม Agent)
        current_flow_id = flow_id or str(uuid.uuid4())

        env = Envelope(
            intent=intent,
            sender_id=self.agent_id,
            payload=payload,
            flow_id=current_flow_id
        )

        logger.debug(f"📤 [Agent: {self.agent_id}] Publishing to '{topic}' | Intent: {intent} | Flow: {current_flow_id}")

        try:
            await self.bus.publish(topic, env)
        except Exception as e:
            logger.error(f"❌ [Agent: {self.agent_id}] Error publishing to '{topic}': {e}")
            # อาจจะเพิ่ม logic การ retry ที่นี่ได้ในอนาคต

    async def start(self):
        """
        Method ที่จะถูก Override โดย Subclass เพื่อเริ่มการทำงานหลัก
        """
        logger.info(f"🚀 [Agent: {self.agent_id}] Starting main loop...")
        pass

    async def stop(self):
        """
        Method สำหรับการเคลียร์ทรัพยากรก่อนปิดตัว
        """
        logger.info(f"🛑 [Agent: {self.agent_id}] Stopping...")
        pass
        
