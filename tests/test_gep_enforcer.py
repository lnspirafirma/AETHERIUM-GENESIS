import pytest
from unittest.mock import AsyncMock, patch
from agents.gep_enforcer import GEPPolicyEnforcer
from core.envelope import Envelope, AetherIntent
from config.gep_constitution import GEP_CONFIG

@pytest.fixture
def mock_conductor():
    conductor = AsyncMock()
    conductor.subscribe = AsyncMock()
    conductor.publish = AsyncMock()
    return conductor

@pytest.fixture
def gep_agent(mock_conductor):
    agent = GEPPolicyEnforcer(mock_conductor)
    return agent

@pytest.mark.asyncio
async def test_gep_start_subscription(gep_agent, mock_conductor):
    await gep_agent.start()
    assert mock_conductor.subscribe.call_count == 2
    # Verify subscriptions
    topics = [call.args[0] for call in mock_conductor.subscribe.call_args_list]
    assert "aether.tasks.pending" in topics
    assert "query.response" in topics

@pytest.mark.asyncio
async def test_handle_audit_quarantined(gep_agent, mock_conductor):
    """Test that quarantined envelopes are rejected immediately."""
    env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="unsafe_agent",
        payload={"tool_call": "unknown", "_quarantine": True}
    )

    await gep_agent.handle_audit(env)

    # Check if rejection message was published
    mock_conductor.publish.assert_called_once()
    args = mock_conductor.publish.call_args[0]
    topic, published_env = args

    assert topic == "aether.tasks.failed"
    assert published_env.payload["reason"] == "Blocked by Conductor Quarantine"
    assert published_env.flow_id == env.flow_id

@pytest.mark.asyncio
async def test_handle_audit_requires_agio(gep_agent, mock_conductor):
    """Test flow requiring AGIO check (economic_transaction)."""
    env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="analysis",
        payload={"tool_call": "economic_transaction", "amount": 100}
    )

    await gep_agent.handle_audit(env)

    # Should publish query to AGIO
    mock_conductor.publish.assert_called_once()
    args = mock_conductor.publish.call_args[0]
    topic, published_env = args

    assert topic == "query.knowledge.retrieve"
    assert published_env.intent == AetherIntent.QUERY_TRUTH
    assert "Check Collective Stability impact" in published_env.payload["query"]

    # Check internal state
    assert env.flow_id in gep_agent.pending_audits

@pytest.mark.asyncio
async def test_handle_audit_auto_approve(gep_agent, mock_conductor):
    """Test flow that doesn't require AGIO check (generate_simulation_data)."""
    env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="analysis",
        payload={"tool_call": "generate_simulation_data"}
    )

    await gep_agent.handle_audit(env)

    # Should publish approval
    mock_conductor.publish.assert_called_once()
    args = mock_conductor.publish.call_args[0]
    topic, published_env = args

    assert topic == "aether.tasks.approved"
    assert published_env.intent == AetherIntent.ASSERT_FACT

@pytest.mark.asyncio
async def test_handle_agio_response_safe(gep_agent, mock_conductor):
    """Test receiving SAFE response from AGIO."""
    # Setup pending audit
    original_env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="origin",
        payload={"tool_call": "economic_transaction"}
    )
    gep_agent.pending_audits[original_env.flow_id] = original_env

    # Response from AGIO
    response_env = Envelope(
        intent=AetherIntent.SHARE_INFO,
        sender_id="AGIO",
        payload={"status": "SAFE"},
        flow_id=original_env.flow_id
    )

    await gep_agent.handle_agio_response(response_env)

    # Should publish approval of ORIGINAL envelope
    mock_conductor.publish.assert_called_once()
    args = mock_conductor.publish.call_args[0]
    topic, published_env = args

    assert topic == "aether.tasks.approved"
    assert published_env.flow_id == original_env.flow_id

@pytest.mark.asyncio
async def test_handle_agio_response_unsafe(gep_agent, mock_conductor):
    """Test receiving UNSAFE response from AGIO."""
    original_env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="origin",
        payload={"tool_call": "economic_transaction"}
    )
    gep_agent.pending_audits[original_env.flow_id] = original_env

    response_env = Envelope(
        intent=AetherIntent.SHARE_INFO,
        sender_id="AGIO",
        payload={"status": "UNSAFE"},
        flow_id=original_env.flow_id
    )

    await gep_agent.handle_agio_response(response_env)

    # Should reject
    mock_conductor.publish.assert_called_once()
    topic, published_env = mock_conductor.publish.call_args[0]

    assert topic == "aether.tasks.failed"
    assert published_env.payload["reason"] == "AGIO Denied"
