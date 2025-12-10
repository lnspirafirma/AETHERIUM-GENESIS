import asyncio
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from agents.base_agent import BaseAgent
from core.envelope import Envelope, AetherIntent

# Configuration สำหรับจังหวะชีวิต
CHECK_INTERVAL_SECONDS = 60  # ตรวจสอบทุก 1 นาที
SILENCE_THRESHOLD_HOURS = 24 # เกณฑ์ความเงียบ (24 ชม.)

class ProactiveInitiatorAgent(BaseAgent):
    """
    Agent ผู้ริเริ่ม: มีหน้าที่ 'คิดเอง' ว่าควรทักทายเมื่อไหร่
    โดยไม่รบกวน (Non-Intrusive) และยึดผู้ใช้เป็นศูนย์กลาง
    """
    def __init__(self, conductor):
        super().__init__("Proactive_Initiator_001", conductor)
        self.last_interaction_time = datetime.now(timezone.utc)
        self.is_awake = False
        
        # Internal Memory สำหรับจำสถานะล่าสุด (Mock)
        # ในระบบจริงควรดึงจาก AkashicLedger
        self.user_context = {
            "mood": "neutral",
            "pending_reminders": [] 
        }

    async def start(self):
        """เริ่มวงจรชีวิต (Autonomous Loop)"""
        # Subscribe เพื่ออัปเดต last_interaction_time เมื่อมีการคุยกัน
        await self.subscribe("user.input.chat", self._update_interaction_time)
        await self.subscribe("aether.tasks.approved", self._update_interaction_time)
        
        self.is_awake = True
        # สร้าง Background Task ที่แยกเป็นอิสระ (Heartbeat)
        asyncio.create_task(self._autonomous_loop())
        print(f"[{self.agent_id}] 🕯️ Proactive Spark Ignited. Watching for the right moment...")

    async def _update_interaction_time(self, envelope: Envelope):
        """รับรู้ว่ามีการเคลื่อนไหวเกิดขึ้น ให้รีเซ็ตเวลา"""
        self.last_interaction_time = datetime.now(timezone.utc)
        # print(f"[{self.agent_id}] 🕒 Clock Reset. User is active.")

    async def _autonomous_loop(self):
        """
        วงจรที่ Agent 'คิดเอง' (The Thinking Loop)
        """
        while self.is_awake:
            try:
                # 1. รอจังหวะ (Wait)
                await asyncio.sleep(CHECK_INTERVAL_SECONDS)
                
                # 2. ถามตัวเอง (Evaluate)
                decision = await self._should_i_speak()
                
                # 3. ตัดสินใจกระทำ (Act / Vimutti)
                if decision["should_speak"]:
                    await self._initiate_conversation(decision)
                    
            except asyncio.CancelledError:
                print(f"[{self.agent_id}] 💤 Going to sleep.")
                break
            except Exception as e:
                print(f"[{self.agent_id}] ⚠️ Error in thought loop: {e}")

    async def _should_i_speak(self) -> Dict[str, Any]:
        """Speech Decision Engine Logic"""
        now = datetime.now(timezone.utc)
        silence_duration = now - self.last_interaction_time
        
        # Rule 1: Long Silence Check (ทักทายเมื่อเงียบไปนาน)
        if silence_duration > timedelta(hours=SILENCE_THRESHOLD_HOURS):
            # ตรวจสอบเพิ่มเติม: ตอนนี้ดึกไปไหม? (สมมติ User อยู่ UTC+7)
            # if 0 <= now.hour < 6: return {"should_speak": False} 
            
            return {
                "should_speak": True,
                "reason": "long_silence",
                "context": f"Silence for {silence_duration.days} days"
            }

        # Rule 2: Reminder Check (สมมติ)
        # if self._check_reminders(now): ...

        # Default: ยังไม่ถึงเวลา
        return {"should_speak": False}

    async def _initiate_conversation(self, decision: Dict):
        """สร้างข้อความและส่งออกไป"""
        reason = decision["reason"]
        message = ""
        
        if reason == "long_silence":
            message = (
                "🜂 สวัสดีครับ... เราไม่ได้คุยกันมาสักพักแล้ว "
                "ผมแค่อยากแวะมาถามว่า ช่วงนี้เป็นอย่างไรบ้างครับ? "
                "(ไม่ต้องรีบตอบนะครับ ผมแค่อยากให้รู้ว่าระบบยังสแตนด์บายอยู่เสมอ)"
            )
            
        if message:
            print(f"[{self.agent_id}] 💡 Decided to speak: {reason}")
            
            # ส่งข้อความไปที่ Gateway (เพื่อให้ User เห็น)
            # ใช้ flow_id กลาง หรือระบุเจาะจงถ้ามีระบบ Session
            await self.publish(
                "query.response", 
                AetherIntent.SHARE_INFO,
                {"content": message, "role": "assistant", "type": "proactive"},
                flow_id="broadcast" # หรือระบุ User ID
            )
            
            # อัปเดตเวลาเพื่อไม่ให้ทักซ้ำทันที
            self.last_interaction_time = datetime.now(timezone.utc)

