from dataclasses import dataclass, field
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json

class AetherIntent(Enum):
    REQUEST_ACTION = "request_action"
    SHARE_INFO = "share_info"
    QUERY_TRUTH = "query_truth"
    ASSERT_FACT = "assert_fact"
    AUDIT_REPORT = "audit_report"

@dataclass(frozen=True)
class AbsoluteTruth:
    global_state_hash: str
    rule_version: str = "GEP-v1.0"

@dataclass
class Envelope:
    intent: AetherIntent
    sender_id: str
    payload: Dict[str, Any]
    context_snapshot: Dict[str, Any] = field(default_factory=dict)

    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    flow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace: List[str] = field(default_factory=list)

    # Devordota/Akashic Integrity
    def get_canonical_hash(self) -> str:
        canonical_data = json.dumps(self.payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_data.encode('utf-8')).hexdigest()
