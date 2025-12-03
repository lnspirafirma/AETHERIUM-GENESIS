from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import hashlib
import json
from typing import Any, Optional

class AkashicEnvelope(BaseModel):
    """
    DNA ของระบบ: บันทึกข้อมูลแบบ Immutable (แก้ไขไม่ได้)
    สอดคล้องกับหลักการ 'ความทรงจำบริสุทธิ์' (Frozen=True)
    """
    id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    intent: str  # เจตนา (Inspira)
    actor: str   # ผู้กระทำ (Agent Name)
    action_type: str # เช่น 'economic_transaction', 'code_generation'
    payload: Any     # ข้อมูลดิบ
    previous_hash: Optional[str] = None # เชื่อมโยงเหมือน Blockchain
    signature: str = "" # ลายเซ็นดิจิทัล (Hash)

    class Config:
        frozen = True # ทำให้ Object นี้แก้ไขไม่ได้หลังจากสร้าง (Immutability)

    @field_validator('signature', mode='before')
    @classmethod
    def generate_signature(cls, v, info):
        # คำนวณ Hash จากข้อมูลทั้งหมดเพื่อยืนยันความถูกต้อง (Integrity Check)
        if v: return v # ถ้ามีลายเซ็นแล้วให้ผ่าน
        
        # ดึงข้อมูลดิบมา Hash
        data = info.data
        raw_string = f"{data.get('id')}{data.get('timestamp')}{data.get('intent')}{data.get('payload')}"
        return hashlib.sha256(raw_string.encode()).hexdigest()

class AkashicLedger:
    """
    สมุดบัญชีแยกประเภทที่บันทึกทุกการกระทำของ AG (Database Layer)
    """
    def __init__(self):
        self._chain = []

    def record(self, envelope: AkashicEnvelope):
        # ตรวจสอบความถูกต้องก่อนบันทึก
        if len(self._chain) > 0:
            last_record = self._chain[-1]
            # (ในระบบจริงต้องเช็ค previous_hash)
        
        self._chain.append(envelope)
        print(f"📜 [AKASHIC]: Recorded Action '{envelope.action_type}' by {envelope.actor} | Hash: {envelope.signature[:8]}...")
  
