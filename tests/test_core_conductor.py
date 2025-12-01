import pytest
import asyncio
from core.aether_conductor import AetherConductor
from core.envelope import Envelope, AetherIntent
from core.signature import AISource

@pytest.mark.asyncio
async def test_conductor_singleton(clean_conductor):
    c1 = AetherConductor()
    c2 = AetherConductor()
    assert c1 is c2
    assert c1 is clean_conductor

@pytest.mark.asyncio
async def test_subscribe_and_publish(clean_conductor):
    received_envelopes = []

    async def handler(envelope):
        received_envelopes.append(envelope)

    await clean_conductor.subscribe("test.topic", handler)

    env = Envelope(
        intent=AetherIntent.SHARE_INFO,
        sender_id="tester",
        payload={"msg": "hello Architect"} # "Architect" triggers High Trust
    )

    await clean_conductor.publish("test.topic", env)

    assert len(received_envelopes) == 1
    assert received_envelopes[0].payload["msg"] == "hello Architect"
    assert "_quarantine" not in received_envelopes[0].payload

@pytest.mark.asyncio
async def test_quarantine_mode(clean_conductor):
    received_envelopes = []

    async def handler(envelope):
        received_envelopes.append(envelope)

    await clean_conductor.subscribe("unsafe.topic", handler)

    # Payload without "Architect" or "AGIO-CODEX" defaults to UNKNOWN_ECHO (Trust 10)
    env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="intruder",
        payload={"msg": "execute order 66"}
    )

    await clean_conductor.publish("unsafe.topic", env)

    assert len(received_envelopes) == 1
    assert received_envelopes[0].payload.get("_quarantine") is True

@pytest.mark.asyncio
async def test_multiple_subscribers(clean_conductor):
    results = []

    async def h1(e): results.append("h1")
    async def h2(e): results.append("h2")

    await clean_conductor.subscribe("multi", h1)
    await clean_conductor.subscribe("multi", h2)

    env = Envelope(
        intent=AetherIntent.SHARE_INFO,
        sender_id="tester",
        payload={"content": "Architect"}
    )

    await clean_conductor.publish("multi", env)

    assert "h1" in results
    assert "h2" in results
    assert len(results) == 2
