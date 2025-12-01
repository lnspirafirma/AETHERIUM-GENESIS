import asyncio
from core.aether_conductor import conductor
from core.envelope import Envelope, AetherIntent
from agents.gep_enforcer import GEPPolicyEnforcer
from agents.agio_sage_agent import AgioSageAgent
from agents.analysis_agent import AnalysisAgent
from agents.resource_agent import ResourceAgent

async def run_simulation():
    print("\n--- 🌌 AETHERIUM GENESIS: AWAKENING SEQUENCE ---")

    # 1. Initialize Governance (The Law)
    gep = GEPPolicyEnforcer(conductor) # Conductor is the new Bus
    await gep.start()

    # 2. Initialize Wisdom (The Mind)
    agio = AgioSageAgent(conductor)
    await agio.start()

    # 3. Initialize Action & Resource (The Body)
    resource = ResourceAgent(conductor)
    await resource.start()

    analysis = AnalysisAgent(conductor)
    await analysis.start()

    print("\n--- ✅ SYSTEM ONLINE: Ready to Process Devordota ---")

    # [Simulation Scenario]
    # 1. Valid Request (Should Pass)
    print("\n[TEST 1] Sending Economic Transaction...")
    await analysis.request_economic_transaction()

    await asyncio.sleep(2) # Allow async processing

    # 2. Invalid Request (Should Block by Retroactive Flow or GEP)
    print("\n[TEST 2] Sending High-Risk Simulation...")
    await analysis.request_simulation_data()

    await asyncio.sleep(2)
    print("\n--- END OF SIMULATION ---")

if __name__ == "__main__":
    asyncio.run(run_simulation())
