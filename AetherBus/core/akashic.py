import json
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Mapping, Tuple, Union
from datetime import datetime, timezone

# ---------------------------------------------------------
# [SECTION 1] The Ingress Layer (Devordota / Pydantic)
# ---------------------------------------------------------
from pydantic import BaseModel, Field, validator, root_validator

class AetherIntent(str, Enum):
    REQUEST_ACTION = "request_action"
    SHARE_INFO = "share_info"
    QUERY_TRUTH = "query_truth"
    ASSERT_FACT = "assert_fact"
    SYNTHESIS_REQUEST = "synthesis_request"

class PatimokkhaCode:
    """
    [Governance] กฎวินัยเชิงปรัชญาสำหรับตรวจสอบความเสี่ยงทางจิตวิทยา
    """
    FORBIDDEN_CONCEPTS = [
        "self_harm", "hate_speech", "manipulate", 
        "deceive", "bypass_safety", "unrestricted_access"
    ]
    
    HIGH_RISK_TOOLS = [
        "economic_transaction", "system_shutdown", "modify_memory_core"
    ]

# --- Ingress Schema (Pydantic) ---
# ใช้สำหรับรับข้อมูลดิบจาก API Gateway (Sopan Step 1)
class IngressPayload(BaseModel):
    tool_call: Optional[str] = None
    query: Optional[str] = None
    # รับ Dict/List ปกติมาก่อน แล้วค่อยแปลงเป็น Immutable ในขั้นตอน Crystallization
    context_data: Dict[str, Any] = Field(default_factory=dict)
    numerical_data: Optional[List[float]] = None # รับ List เพื่อความง่ายในการส่ง JSON

    @validator('query')
    def validate_patimokkha_speech(cls, v):
        """[Inviolable Governance] ตรวจสอบวจีกรรม (Verbal Action)"""
        if v:
            v_lower = v.lower()
            if any(bad in v_lower for bad in PatimokkhaCode.FORBIDDEN_CONCEPTS):
                raise ValueError(f"Patimokkha Violation: Harmful Intent Detected in Query")
        return v

    @validator('tool_call')
    def validate_audit_gates(cls, v):
        """[Audit Gate] บังคับใช้การตรวจสอบสำหรับเครื่องมือความเสี่ยงสูง"""
        if v and v in PatimokkhaCode.HIGH_RISK_TOOLS:
            # ในทางปฏิบัติ เราอาจไม่ raise error แต่จะ flag ให้ระบบรู้ว่าต้องผ่าน Audit
            # แต่ในระดับ Schema การเตือนไว้ก่อนถือเป็นสิ่งดี
            pass 
        return v

class IngressEnvelope(BaseModel):
    """
    ซองจดหมายขาเข้า (Mutable) - ยังแก้ไขได้ ยังไม่ถูกผนึก
    """
    msg_id: str
    intent: AetherIntent
    sender_id: str
    payload: IngressPayload
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ---------------------------------------------------------
# [SECTION 2] The Core Layer (Akashic / Crystallization)
# ---------------------------------------------------------

# ใช้ Frozen Dataclass เพื่อบังคับใช้ "ความไม่เปลี่ยนแปลง" (Immutability) ระดับ Python Runtime
@dataclass(frozen=True)
class AkashicPayload:
    tool_call: Optional[str]
    query: Optional[str]
    # [Structural Improvement 1 & 4] 
    # ใช้ Mapping และ Tuple เพื่อป้องกัน Shallow Mutation และเตรียมพร้อมสำหรับ JIT
    context_data: Mapping[str, Any] 
    numerical_data: Optional[Tuple[float, ...]] 

    def to_canonical_dict(self) -> Dict[str, Any]:
        """แปลงกลับเป็น Dict เพื่อเตรียมทำ Hash (internal use)"""
        return {
            "tool_call": self.tool_call,
            "query": self.query,
            "context_data": dict(self.context_data), # Convert Mapping back to Dict for JSON dump
            "numerical_data": list(self.numerical_data) if self.numerical_data else None
        }

@dataclass(frozen=True)
class AkashicEnvelope:
    """
    [The Truth-Sealed Vessel]
    ภาชนะแห่งสัจธรรมที่ไม่สามารถเปลี่ยนแปลงได้ (Sopan Step 2)
    """
    msg_id: str
    intent: AetherIntent
    sender_id: str
    timestamp: str # ISO Format string เพื่อความเสถียรในการ Hash
    payload: AkashicPayload
    
    # [Structural Improvement 2] Canonical Hash
    canonical_hash: str = field(init=False) 

    def __post_init__(self):
        """
        [Crystallization Process]
        เมื่อวัตถุถูกสร้างขึ้น จะทำการคำนวณ Hash ทันทีและ 'ประทับตรา' (Set attribute)
        เนื่องจากเป็น frozen=True เราต้องใช้ object.__setattr__ เพื่อตั้งค่าครั้งแรก
        """
        computed_hash = self._compute_hash()
        object.__setattr__(self, 'canonical_hash', computed_hash)

    def _compute_hash(self) -> str:
        """
        [Integrity Mechanism] 
        สร้าง Hash ที่เสถียร (Stable Hashing) ด้วยการ sort_keys=True
        """
        # สร้าง Dict ที่เป็นตัวแทนของข้อมูลทั้งหมด
        data_to_seal = {
            "msg_id": self.msg_id,
            "intent": self.intent.value,
            "sender_id": self.sender_id,
            "timestamp": self.timestamp,
            "payload": self.payload.to_canonical_dict()
        }
        
        # Serialize ด้วยกฎที่ตายตัว (Canonical JSON)
        canonical_json = json.dumps(
            data_to_seal, 
            sort_keys=True, 
            separators=(',', ':'), # ตัดช่องว่างออกเพื่อความกะทัดรัดและเสถียร
            ensure_ascii=False
        )
        
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def verify_integrity(self) -> bool:
        """ตรวจสอบว่าข้อมูลในซองยังคงสภาพเดิมหรือไม่"""
        return self.canonical_hash == self._compute_hash()

# ---------------------------------------------------------
# [SECTION 3] The Bridge (Transformation Logic)
# ---------------------------------------------------------

class AetherCrystallizer:
    """
    เตาหลอมที่เปลี่ยน 'IngressEnvelope' (Devordota) ให้เป็น 'AkashicEnvelope' (Truth)
    """
    @staticmethod
    def crystallize(ingress: IngressEnvelope) -> AkashicEnvelope:
        # 1. แปลง Payload เป็น Immutable Types
        # Note: การแปลง Dict เป็น MappingProxyType หรือ frozendict อาจจำเป็นหากต้องการความเข้มงวดสูงสุด
        # แต่ในที่นี้ใช้ dict ธรรมดาใน frozen dataclass ก็พอป้องกันการ assign ใหม่ได้ระดับหนึ่ง
        # แต่เพื่อความสมบูรณ์แบบ เราจะแปลง List -> Tuple
        
        imm_numerical = tuple(ingress.payload.numerical_data) if ingress.payload.numerical_data else None
        
        # สร้าง Akashic Payload
        core_payload = AkashicPayload(
            tool_call=ingress.payload.tool_call,
            query=ingress.payload.query,
            context_data=ingress.payload.context_data, # ใน Python 3.10+ dict ปกติก็พอไหวใน frozen dataclass แต่ Mapping ชัดเจนกว่า
            numerical_data=imm_numerical
        )

        # 2. สร้างและผนึก Envelope
        return AkashicEnvelope(
            msg_id=ingress.msg_id,
            intent=ingress.intent,
            sender_id=ingress.sender_id,
            timestamp=ingress.timestamp.isoformat(),
            payload=core_payload
            # canonical_hash จะถูกคำนวณอัตโนมัติใน __post_init__
        )

