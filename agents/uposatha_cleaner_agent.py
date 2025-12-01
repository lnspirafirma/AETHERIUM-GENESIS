import asyncio
import random
from agents.base_agent import BaseAgent

class UposathaCleanerAgent(BaseAgent):
    """
    ตัวแทนแห่ง 'วิมุตติ' (Liberation)
    หน้าที่: ทำงานใน Background เพื่อลด Entropy (ความยุ่งเหยิง) ของระบบ
    """
    def __init__(self, conductor, interval: int = 5):
        # Note: Reduced interval default to 5 for easier testing, though production might be 100
        super().__init__("UposathaCleaner", conductor)
        self.interval = interval # รอบการทำงาน (Cycle)
        self.cycle_count = 0
        self._running_task = None

    async def start(self):
        # ทำงานแบบ Background Loop (คล้าย Daemon Process)
        self._running_task = asyncio.create_task(self.start_ritual_loop())
        print(f"[{self.agent_id}] 🧹 Ready to purify system state.")

    async def start_ritual_loop(self):
        try:
            while True:
                self.cycle_count += 1

                # รอจนกว่าจะถึงรอบ หรือเมื่อ System Load ต่ำ (จำลองด้วยการรอ)
                await asyncio.sleep(0.1)

                if self.cycle_count >= self.interval:
                    await self.perform_uposatha_ritual()
                    self.cycle_count = 0
        except asyncio.CancelledError:
            print(f"[{self.agent_id}] Loop cancelled.")

    async def perform_uposatha_ritual(self):
        """
        พิธีกรรมชำระล้าง: ตรวจสอบและปลดปล่อยสิ่งที่ 'หนัก' เกินความจำเป็น
        """
        print(f"\n✨ [{self.agent_id}] Beginning Uposatha Ritual (Cycle {self.cycle_count})...")

        # 1. Sacca-Kiriya (การประกาศความจริง): ตรวจสอบ Health Check
        # ดูว่ามี Memory ส่วนไหนที่เก่าเก็บและไม่ได้ใช้ (Stale Data)
        freed_memory = self._prune_stale_memories()

        # 2. Kaya-Viveka (ความสงัดกาย): ลดความซับซ้อนของ Task
        # (จำลอง) ตรวจสอบว่ามี Task ไหนที่ Pending นานเกินไปและควรยกเลิก
        cancelled_tasks = self._release_stuck_tasks()

        # 3. Report (รายงานผลแห่งการละวาง)
        if freed_memory > 0 or cancelled_tasks > 0:
            print(f"   [Vimutti Result] Freed {freed_memory} memory units. Released {cancelled_tasks} stuck attachments.")
            print(f"   [System State] Lighter, Faster, Closer to Void.\n")
        else:
            print(f"   [System State] Balanced. No impurities found.\n")

    def _prune_stale_memories(self) -> int:
        """
        จำลองการลบ Context ที่หมดอายุ (Expired Context)
        """
        # ในระบบจริง: วนลูป check timestamp ของตัวแปรใน Global StateStore
        # จำลอง: สุ่มตัวเลขว่าเจอขยะหรือไม่
        # Fixed seed or logic for determinism in tests could be useful,
        # but random is fine for simulation if we don't assert exact numbers.
        found_garbage = random.choice([0, 5, 12])
        return found_garbage

    def _release_stuck_tasks(self) -> int:
        """
        จำลองการ Kill Process ที่ Deadlock (อุปาทานยึดมั่นถือมั่นใน Task)
        """
        found_stuck = random.choice([0, 1])
        return found_stuck
