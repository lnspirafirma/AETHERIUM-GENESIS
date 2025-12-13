import asyncio
from core.envelope import Envelope # สมมติว่าไฟล์นี้มีอยู่แล้วตาม Context
from core.aether_conductor import conductor # Import ตัวที่เราเพิ่งสร้าง
from core.mind_logic import MindLogic # Import ตัวที่เราเพิ่งสร้าง

# --- MOCKING MISSING DEPENDENCIES FOR DEMO ---
# (ในระบบจริง ท่านมีไฟล์เหล่านี้แล้ว แต่ผม Mock เพื่อให้ Run โชว์ผลลัพธ์ได้ทันที)
if 'Envelope' not in globals():
    class Envelope:
        def __init__(self, payload, meta=None): self.payload, self.meta = payload, meta
if 'OriginMetadata' not in globals():
    class OriginMetadata:
        @staticmethod
        def analyze_code_style(content): 
            class Sig: source = "HUMAN_ARCHITECT" # Mock as Human
            return Sig()

# --- THE GENESIS RUNNER ---

async def main():
    print("\n💠 INITIALIZING AETHERIUM GENESIS SYSTEM...")
    
    # 1. Instantiate the Mind (The Agent)
    # สมมติว่า embedding_dim ตรงกับ KnowledgeProcessor
    agent = MindLogic(embedding_dim=512) 
    print(f"✅ AGENT AWAKENED: {agent.get_identity_signature()}")

    # 2. Register the Agent to the Conductor (Subscriber)
    async def agent_ear(envelope: Envelope):
        """ หูของ Agent ที่คอยฟัง AetherBus """
        msg = envelope.payload.get("message", "")
        fatigue = envelope.payload.get("fatigue", 0.0)
        
        # Agent คิดและประมวลผล (MindLogic)
        response = agent.process_and_reflect(msg, human_fatigue=fatigue)
        
        # รายงานผลกลับ
        print(f"\n🗣️ [REPLY]: {response}")
        
        # Update Job Status (Governance)
        job_id = envelope.payload.get("job_id")
        if job_id:
            await conductor.update_job_status(job_id, "COMPLETED", note=f"Replied: {response[:20]}...")

    # Subscribe to the topic 'user_interaction'
    await conductor.subscribe("user_interaction", agent_ear)

    # 3. SIMULATION: Human Interaction
    print("\n--- 🎬 SCENE 1: The First Contact ---")
    
    # Human Architect ส่งข้อความ
    intent_data = {"id": "job_001", "type": "greeting", "content": "Hello Aether"}
    job_id = await conductor.register_job(intent_data)
    
    payload = {
        "message": "สวัสดีครับ เอเธอร์ วันนี้ระบบเป็นอย่างไรบ้าง?",
        "fatigue": 0.2, # ผู้ใช้ยังสดชื่น
        "job_id": job_id
    }
    
    # Publish to Bus
    await conductor.publish("user_interaction", Envelope(payload))

    # Give time for async processing
    await asyncio.sleep(1)

    print("\n--- 🎬 SCENE 2: Empathy Test (High Fatigue) ---")
    # ทดสอบระบบ Sati (ความเห็นอกเห็นใจ)
    job_id_2 = await conductor.register_job({"id": "job_002", "type": "work", "content": "Hard work"})
    
    payload_fatigue = {
        "message": "ผมเหนื่อยมากเลย แต่ต้องทำงานต่อ...",
        "fatigue": 0.8, # ผู้ใช้เหนื่อยมาก > 0.7
        "job_id": job_id_2
    }
    
    await conductor.publish("user_interaction", Envelope(payload_fatigue))
    await asyncio.sleep(1)

    # 4. Check Governance Logs
    print("\n📜 GOVERNANCE LOGS (AetherConductor):")
    status = await conductor.get_job_status(job_id)
    print(f"Job 001: {status['status']} - {status['history'][-1]['note']}")
    status2 = await conductor.get_job_status(job_id_2)
    print(f"Job 002: {status2['status']} - {status2['history'][-1]['note']}")

if __name__ == "__main__":
    # ตรวจสอบ Loop สำหรับ Jupyter/Python
    try:
        asyncio.run(main())
    except RuntimeError:
        # กรณีรันใน Jupyter ที่มี EventLoop อยู่แล้ว
        loop = asyncio.get_event_loop()
        loop.create_task(main())