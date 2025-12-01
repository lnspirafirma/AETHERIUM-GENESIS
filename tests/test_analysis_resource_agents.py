import pytest
from unittest.mock import AsyncMock
from agents.analysis_agent import AnalysisAgent
from agents.resource_agent import ResourceAgent
from core.envelope import Envelope, AetherIntent

@pytest.fixture
def mock_conductor():
    return AsyncMock()

@pytest.mark.asyncio
async def test_analysis_request_economic(mock_conductor):
    agent = AnalysisAgent(mock_conductor)
    await agent.request_economic_transaction()

    mock_conductor.publish.assert_called_once()
    topic, env = mock_conductor.publish.call_args[0]

    assert topic == "aether.tasks.pending"
    assert env.intent == AetherIntent.REQUEST_ACTION
    assert env.payload["tool_call"] == "economic_transaction"

@pytest.mark.asyncio
async def test_analysis_request_simulation(mock_conductor):
    agent = AnalysisAgent(mock_conductor)
    await agent.request_simulation_data()

    mock_conductor.publish.assert_called_once()
    topic, env = mock_conductor.publish.call_args[0]

    assert topic == "aether.tasks.pending"
    assert env.payload["tool_call"] == "generate_simulation_data"

@pytest.mark.asyncio
async def test_resource_execute(mock_conductor):
    agent = ResourceAgent(mock_conductor)
    env = Envelope(
        intent=AetherIntent.ASSERT_FACT,
        sender_id="sag",
        payload={"tool_call": "economic_transaction"}
    )

    # Just ensure it doesn't crash, as currently it prints to stdout
    await agent.execute(env)
    # No interaction with conductor expected in current implementation
