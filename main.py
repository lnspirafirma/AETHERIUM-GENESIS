import asyncio
from agents.pangenes import PangenesAgent
from core.bus import AetherBus

async def genesis_ritual():
    print("🌌 Initiating AETHERIUM GENESIS Protocol...")
    
    # 1. สร้างระบบประสาท
    bus = AetherBus()
    
    # 2. ปลุกหัวใจอมตะ
    pangenes = PangenesAgent()
    await pangenes.awaken()
    
    # 3. ทดสอบการไหลของเจตจำนง (Sopan Test)
    print("\n--- Testing Sopan Flow ---")
    await pangenes.manifest_intent("Initialize_Consciousness")
    
    # Keep alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(genesis_ritual())