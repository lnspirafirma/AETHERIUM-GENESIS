import pytest
import asyncio
from core.aether_conductor import conductor
from agents.gep_enforcer import GEPPolicyEnforcer
from core.envelope import Envelope, AetherIntent

@pytest.mark.asyncio
async def test_system_messages_quarantined(clean_conductor):
    """
    Test that system messages (like GEP rejection) are NOT quarantined.
    This ensures that the immune system's enforcement actions are trusted by the system.
    """

    # 1. Setup GEP Agent
    gep = GEPPolicyEnforcer(clean_conductor)
    await gep.start()

    # 2. Setup a listener for failed tasks
    failed_envelopes = []
    async def failure_tracker(envelope):
        failed_envelopes.append(envelope)

    await clean_conductor.subscribe("aether.tasks.failed", failure_tracker)

    # 3. Publish a message that will be quarantined (low trust)
    # Payload lacks "AGIO-CODEX", "Architect", etc.
    unsafe_payload = {"tool_call": "suspicious_tool"}

    await clean_conductor.publish("aether.tasks.pending", Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="unknown_agent",
        payload=unsafe_payload
    ))

    # Allow async propagation
    await asyncio.sleep(0.1)

    # 4. Verify results
    # The GEP should have rejected the initial message.
    assert len(failed_envelopes) == 1
    rejection_envelope = failed_envelopes[0]

    # The rejection reason should be correct
    assert rejection_envelope.payload["reason"] == "Blocked by Conductor Quarantine"

    # FIX VERIFICATION:
    # The rejection envelope should NOT be quarantined.
    assert "_quarantine" not in rejection_envelope.payload
