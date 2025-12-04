import asyncio
import time
import random
import sys
import logging
from typing import List, Union, Any

# --- Global Configurations ---
# กำหนดจำนวน Task ที่รันพร้อมกันได้สูงสุด (Rate Limiting)
MAX_CONCURRENT_TASKS = 10 
SEMAPHORE = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
MAX_RETRIES = 3 # จำนวนครั้งสูงสุดที่พยายามลองใหม่
RETRY_BASE_DELAY = 0.5 # เวลาหน่วงพื้นฐานสำหรับการลองใหม่

# --- Logging Configuration ---
# ตั้งค่า Log ให้แสดงแค่ข้อความที่สำคัญระดับ INFO ขึ้นไป
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

class ConnectionFailed(Exception):
    """Custom exception สำหรับการเชื่อมต่อล้มเหลวหลังจากลองใหม่ครบทุกครั้ง"""
    pass

async def cognitive_pulse(task_id: int, speed_mode: str = "NORMAL") -> str:
    """
    จำลองการรอ I/O พร้อมกลไก Semaphore และ Retry (Exponential Backoff)
    """
    # ใช้ Semaphore เพื่อจำกัดจำนวน Task ที่รันพร้อมกัน (ควบคุม Concurrency)
    async with SEMAPHORE:
        for attempt in range(MAX_RETRIES):
            try:
                # กำหนดเวลาหน่วง
                delay = random.uniform(0.1, 0.3) if speed_mode == "LIGHTSPEED" else random.uniform(1.0, 2.0)

                # จำลองการเกิดข้อผิดพลาดแบบสุ่ม: โอกาสลดลงในการลองครั้งถัดไป
                if random.random() < 0.1 / (attempt + 1): 
                    logger.warning(f"Task {task_id} - Attempt {attempt+1}: ❌ Connection lost. Retrying...")
                    # เราจะใช้ ConnectionError เพื่อให้ระบบลองใหม่
                    raise ConnectionError(f"Connection Error on Task {task_id}")

                # จำลองการรอ I/O (แทนการเรียก API)
                await asyncio.sleep(delay) 
                
                # ถ้าสำเร็จ
                return f"⚡ Task {task_id} Completed in {delay:.4f}s (Attempt {attempt+1})"

            except ConnectionError as e:
                # หากยังไม่ครบจำนวนลองใหม่
                if attempt < MAX_RETRIES - 1:
                    # Exponential Backoff with Jitter: หน่วงเวลาเพิ่มขึ้นเรื่อยๆ 
                    backoff_delay = RETRY_BASE_DELAY * (2 ** attempt) + random.uniform(0, 0.2)
                    # logger.debug(f"Task {task_id} - Backing off for {backoff_delay:.2f}s") # สามารถเปิด Log นี้ได้หากต้องการดูดีเทล
                    await asyncio.sleep(backoff_delay)
                    continue
                else:
                    # ล้มเหลวหลังจากลองใหม่ครบทุกครั้ง
                    error_msg = f"🚨 Task {task_id} Failed after {MAX_RETRIES} retries."
                    logger.error(error_msg)
                    raise ConnectionFailed(error_msg) from e
    
    # เพื่อให้แน่ใจว่าฟังก์ชัน return ค่าเสมอ
    raise ConnectionFailed(f"🚨 Task {task_id} Failed unexpectedly (Logic error).")


async def activate_triple_x_mode():
    """
    เริ่มต้นโปรโตคอลความเร็ว TRIPLE-X พร้อมจัดการข้อผิดพลาด
    """
    NUM_TASKS = 50
    logger.info(f"🚀 Starting TRIPLE-X Speed Protocol (Concurrency: {MAX_CONCURRENT_TASKS} tasks)...")
    start_time = time.time()

    # สร้าง Coroutine Objects (แทนการใช้ asyncio.create_task)
    tasks = [cognitive_pulse(i, speed_mode="LIGHTSPEED") for i in range(NUM_TASKS)]

    # สั่งให้ประมวลผลพร้อมกัน และรับค่า Exception หากมี Task ล้มเหลว
    results: List[Union[str, Exception]] = await asyncio.gather(*tasks, return_exceptions=True)

    total_time = time.time() - start_time

    # --- Process Results ---
    successful_results: List[str] = [r for r in results if isinstance(r, str)]
    failed_results: List[Exception] = [r for r in results if isinstance(r, Exception)]

    # --- Summary ---
    logger.info("\n--- Summary ---")
    logger.info(f"✅ Successful tasks: {len(successful_results)} / {NUM_TASKS}")
    logger.info(f"❌ Failed tasks: {len(failed_results)}")

    if failed_results:
        connection_failed_count = sum(1 for r in failed_results if isinstance(r, ConnectionFailed))

        logger.info(f"   -> {connection_failed_count} x ConnectionFailed (Failed after retries)")
        
    logger.info(f"\n⏱️ Total Execution Time: {total_time:.4f}s")

    # Efficiency calculation (approximate)
    average_normal_delay = 1.5 # ค่าเฉลี่ยหน่วงเวลาปกติ (1.0 ถึง 2.0)
    efficiency_gain = (NUM_TASKS * average_normal_delay) / total_time
    logger.info(f"💡 Efficiency Gain: ~{efficiency_gain:.1f}x Faster (vs Linear)")

# --- Main Execution ---
if __name__ == "__main__":
    if sys.version_info < (3, 7):
        logger.critical("Error: This code requires Python 3.7 or newer for full asyncio support.")
    else:
        try:
            asyncio.run(activate_triple_x_mode())
        except KeyboardInterrupt:
            logger.info("\n🛑 Program interrupted by user.")
            
