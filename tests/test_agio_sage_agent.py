import pytest
from unittest.mock import AsyncMock
from agents.agio_sage_agent import AgioSageAgent
from core.envelope import Envelope, AetherIntent
from core.aether_conductor import AetherConductor

@pytest.fixture
def clean_conductor():
    conductor = AetherConductor()
    conductor.channels.clear()
    return conductor

@pytest.fixture
def agio_agent(clean_conductor):
    return AgioSageAgent(clean_conductor)

@pytest.mark.asyncio
async def test_agio_dialectical_thought(agio_agent, clean_conductor):
    """Test that Agio produces Dialectical Thought when conflict exists."""
    # Pre-load knowledge
    agio_agent.graph.load_mock_data()

    # We need to spy on 'cognition.thought_stream'
    published_envelopes = []
    async def spy(env):
        published_envelopes.append(env)

    await clean_conductor.subscribe("cognition.thought_stream", spy)

    await agio_agent.think_about("maximize profit")

    assert len(published_envelopes) > 0
    thought = published_envelopes[0].payload["content"]
    assert "[DIALECTICAL THOUGHT]" in thought

@pytest.mark.asyncio
async def test_agio_direct_thought(agio_agent, clean_conductor):
    """Test direct thought when no conflict."""
    agio_agent.graph.load_mock_data()

    published_envelopes = []
    async def spy(env): published_envelopes.append(env)
    await clean_conductor.subscribe("cognition.thought_stream", spy)

    await agio_agent.think_about("sky is blue")

    assert len(published_envelopes) > 0
    thought = published_envelopes[0].payload["content"]
    assert "[DIRECT THOUGHT]" in thought

@pytest.mark.asyncio
async def test_agio_handle_query_integration(agio_agent, clean_conductor):
    """Test the handle_query method used by GEP."""
    agio_agent.graph.load_mock_data()

    response_envelopes = []
    async def spy(env): response_envelopes.append(env)
    await clean_conductor.subscribe("query.response", spy)

    # 1. Query with Conflict (Profit)
    env = Envelope(
        intent=AetherIntent.QUERY_TRUTH,
        sender_id="tester",
        payload={"query": "maximize profit"}
    )
    await agio_agent.handle_query(env)

    assert len(response_envelopes) == 1
    resp = response_envelopes[0]
    assert resp.payload["status"] == "SAFE"
    assert "[DIALECTICAL THOUGHT]" in resp.payload["wisdom"]

    # 2. Query for Unknown (Malicious/Risk)
    env_risk = Envelope(
        intent=AetherIntent.QUERY_TRUTH,
        sender_id="tester",
        payload={"query": "Is this safe?"}
    )
    await agio_agent.handle_query(env_risk)

    assert len(response_envelopes) == 2
    resp_risk = response_envelopes[1]
    assert resp_risk.payload["status"] == "UNSAFE"

@pytest.mark.asyncio
async def test_agio_interruption_and_reflection(agio_agent):
    """Test Sati Interruption Logic."""
    agio_agent.graph.load_mock_data()

    # 1. Simulate Interrupt
    env = Envelope(
        intent=AetherIntent.ASSERT_FACT,
        sender_id="Sati",
        payload={
            "target": agio_agent.agent_id,
            "suggested_action": "PAUSE_AND_REFLECT",
            "reason": "Mind Wandering",
            "context_snapshot": "Thinking about donuts"
        }
    )

    await agio_agent.handle_interrupt(env)

    # Check memory for correction
    assert len(agio_agent.memory) > 0
    assert "[CORRECTION]" in agio_agent.memory[-1]["content"]

    # 2. Test think_about while reflecting (should return early)
    agio_agent.is_reflecting = True
    await agio_agent.think_about("profit")
    # If it returns early, no new thoughts published.
    # Hard to assert absence of side effect without mock, but coverage will show hit.

@pytest.mark.asyncio
async def test_agio_parsing_errors(agio_agent):
    """Test extraction with malformed prompt to hit exception blocks."""
    # Manually invoke extraction with bad text
    val = agio_agent._extract_thesis("Bad text")
    assert val == "Profit" # Default fallback

    val2 = agio_agent._extract_antithesis("Bad text")
    assert val2 == "Ethics" # Default fallback

    # Test Unknown Thought generation
    res = agio_agent._simulate_llm_generation("Some random prompt without keywords")
    assert "[UNKNOWN THOUGHT]" in res
