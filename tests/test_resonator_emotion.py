import pytest
import asyncio
from agents.aetheric_resonator_agent import AethericResonatorAgent
from core.envelope import Envelope, AetherIntent
from core.aether_conductor import conductor

class MockConductor:
    def __init__(self):
        self.published = []
        self.subscribers = {}

    async def subscribe(self, topic, handler):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def publish(self, topic, envelope):
        self.published.append((topic, envelope))
        # Direct callback simulation
        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                await handler(envelope)

@pytest.mark.asyncio
async def test_resonator_emotion_sensing():
    # Setup
    mock_bus = MockConductor()
    resonator = AethericResonatorAgent(mock_bus)
    await resonator.start()

    # Simulate incoming thought with "Joy" keyword
    payload = {"content": "I am so happy with this success!"}
    env = Envelope(AetherIntent.SHARE_INFO, "Tester", payload)

    # Inject directly
    await resonator.handle_wave_input(env)

    # Buffer should have 1 item
    assert len(resonator.echo_buffer) == 1
    # Emotion shouldn't be set yet (wait for echo) or detected internally?
    # The agent internal _sense_emotion logic is synchronous.
    assert resonator._sense_emotion(str(payload)) == "Joy"

@pytest.mark.asyncio
async def test_resonator_buffer_overflow_resonance():
    # Setup
    mock_bus = MockConductor()
    resonator = AethericResonatorAgent(mock_bus)
    await resonator.start()

    # Fill buffer to limit (5)
    for i in range(5):
        await resonator.handle_wave_input(Envelope(AetherIntent.SHARE_INFO, "Tester", {"msg": f"msg {i}"}))

    assert len(resonator.echo_buffer) == 5
    assert len(mock_bus.published) == 0 # No resonance yet

    # Add 6th item -> Trigger Resonance (Pop first)
    # Use keyword "The Will" -> "Desire"
    trigger_payload = {"msg": "This is The Will of the system"}
    await resonator.handle_wave_input(Envelope(AetherIntent.SHARE_INFO, "Tester", trigger_payload))

    assert len(resonator.echo_buffer) == 5 # Popped one, added one

    # Check published resonance
    # Look for "cognition.resonance"
    resonances = [p for p in mock_bus.published if p[0] == "cognition.resonance"]
    assert len(resonances) == 1

    payload = resonances[0][1].payload
    assert payload["status"] == "RESONATING"
    assert payload["emotion"] == "Desire" # Detected from the trigger msg
    assert "msg 0" in payload["source_echo"] # The oldest message popped
