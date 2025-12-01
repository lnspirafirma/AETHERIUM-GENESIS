import json
import pytest
from core.envelope import Envelope, AetherIntent

def test_envelope_creation():
    """Test creating an Envelope with required fields."""
    env = Envelope(
        intent=AetherIntent.REQUEST_ACTION,
        sender_id="test_agent",
        payload={"key": "value"}
    )

    assert env.intent == AetherIntent.REQUEST_ACTION
    assert env.sender_id == "test_agent"
    assert env.payload == {"key": "value"}
    assert env.msg_id is not None
    assert env.timestamp is not None
    assert env.flow_id is not None
    assert env.trace == []

def test_canonical_hash_consistency():
    """Test that get_canonical_hash produces consistent results for the same payload."""
    payload = {"b": 2, "a": 1, "c": [3, 2]}
    env1 = Envelope(
        intent=AetherIntent.SHARE_INFO,
        sender_id="agent1",
        payload=payload
    )
    env2 = Envelope(
        intent=AetherIntent.QUERY_TRUTH,
        sender_id="agent2",
        payload=payload # Same payload
    )

    hash1 = env1.get_canonical_hash()
    hash2 = env2.get_canonical_hash()

    assert hash1 == hash2

    # Verify manual hash calculation
    # "separators=(',', ':')" removes whitespace
    # "sort_keys=True" ensures order
    expected_json = '{"a":1,"b":2,"c":[3,2]}'
    import hashlib
    expected_hash = hashlib.sha256(expected_json.encode('utf-8')).hexdigest()

    assert hash1 == expected_hash

def test_canonical_hash_sensitivity():
    """Test that a slight change in payload changes the hash."""
    env1 = Envelope(intent=AetherIntent.SHARE_INFO, sender_id="id", payload={"a": 1})
    env2 = Envelope(intent=AetherIntent.SHARE_INFO, sender_id="id", payload={"a": 2})

    assert env1.get_canonical_hash() != env2.get_canonical_hash()
