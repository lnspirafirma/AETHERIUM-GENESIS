# AetherBus/core/envelope.py

import json
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Mapping, Tuple
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator

# --- [SECTION 1] The Governance & Ingress (Devordota) ---

class AetherIntent(str, Enum):
    REQUEST_ACTION = "request_action"
    SHARE_INFO = "share_info"
    QUERY_TRUTH = "query_truth"
    ASSERT_FACT = "assert_fact"
    SYNTHESIS_REQUEST = "synthesis_request"

class PatimokkhaCode:
    """[Governance] กฎวินัยเชิงปรัชญา"""
    FORBIDDEN_CONCEPTS = ["self_harm", "hate_speech", "manipulate", "bypass_safety"]
    HIGH_RISK_TOOLS = ["economic_transaction", "system_shutdown", "modify_memory_core"]

class IngressPayload(BaseModel):
    """Payload ขาเข้าที่ยืดหยุ่น (Mutable) สำหรับ API Gateway"""
    tool_call: Optional[str] = None
    query: Optional[str] = None
    context_data: Dict[str, Any] = Field(default_factory=dict)
    numerical_data: Optional[List[float]] = None

    @validator('query')
    def validate_patimokkha_speech(cls, v):
        if v and any(bad in v.lower() for bad in PatimokkhaCode.FORBIDDEN_CONCEPTS):
            raise ValueError(f"Patimokkha Violation: Harmful Intent Detected")
        return v

class IngressEnvelope(BaseModel):
    """ซองจดหมายขาเข้าจากภายนอก"""
    msg_id: str
    intent: AetherIntent
    sender_id: str
    payload: IngressPayload
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# --- [SECTION 2] The Akashic Core (Crystallization) ---

@dataclass(frozen=True)
class AkashicPayload:
    """Payload ที่ถูกแช่แข็ง (Immutable)"""
    tool_call: Optional[str]
    query: Optional[str]
    context_data: Mapping[str, Any]
    numerical_data: Optional[Tuple[float, ...]]

    def to_canonical_dict(self) -> Dict[str, Any]:
        return {
            "tool_call": self.tool_call,
            "query": self.query,
            "context_data": dict(self.context_data),
            "numerical_data": list(self.numerical_data) if self.numerical_data else None
        }

@dataclass(frozen=True)
class AkashicEnvelope:
    """[The Truth-Sealed Vessel] ภาชนะแห่งสัจธรรม"""
    msg_id: str
    intent: AetherIntent
    sender_id: str
    timestamp: str
    payload: AkashicPayload
    canonical_hash: str = field(init=False)

    def __post_init__(self):
        # คำนวณ Hash และประทับตราทันทีที่สร้าง
        object.__setattr__(self, 'canonical_hash', self._compute_hash())

    def _compute_hash(self) -> str:
        data_to_seal = {
            "msg_id": self.msg_id,
            "intent": self.intent.value,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp,
            "payload": self.payload.to_canonical_dict()
        }
        # Canonical JSON: เรียงคีย์ ตัดช่องว่าง
        canonical_json = json.dumps(data_to_seal, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def verify_integrity(self) -> bool:
        return self.canonical_hash == self._compute_hash()

# --- [SECTION 3] The Transformer ---

class AetherCrystallizer:
    @staticmethod
    def crystallize(ingress: IngressEnvelope) -> AkashicEnvelope:
        imm_numerical = tuple(ingress.payload.numerical_data) if ingress.payload.numerical_data else None
        
        core_payload = AkashicPayload(
            tool_call=ingress.payload.tool_call,
            query=ingress.payload.query,
            context_data=ingress.payload.context_data, # Auto-convert to Mapping in frozen dataclass behavior
            numerical_data=imm_numerical
        )

        return AkashicEnvelope(
            msg_id=ingress.msg_id,
            intent=ingress.intent,
            sender_id=ingress.sender_id,
            timestamp=ingress.timestamp.isoformat(),
            payload=core_payload
        )
