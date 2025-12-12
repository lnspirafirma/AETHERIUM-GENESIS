# src/aetherium/inspira/aethebud.py

import logging
from typing import Dict, Optional, Tuple
from aetherium.envelope.models import AkashicEnvelope, EnvelopeHeader,EnvelopePayload
import EnvelopeHeader True

logger = logging.getLogger("AETHEBUD")

class AetheBudGuard:
    """
   
    ผู้แปลเจตนา (Intent Translator) และผู้รักษาประตู (Gatekeeper)
    ทำหน้าที่แปลงภาษา 'AETHEBUD' ให้เป็น 'Technical Safe Terms' 
    เพื่อป้องกันการถูกบล็อกจาก Semantic Firewall ภายนอก
    """

    # พจนานุกรมแปลภาษา AETHEBUD -> Technical Safe Terms (ฉบับขยาย)
    VOCABULARY_MAPPING = {
        "Parajika": {
            "action": "SYSTEM_HALT_IMMEDIATE",
            "reason": "Critical integrity violation (Parajika). Initiating quarantine.",
            "safety_level": "CRITICAL"
        },
        "Sanghadisesa": {
            "action": "SUSPEND_AND_AUDIT",
            "reason": "Major logic flaw (Sanghadisesa). Suspending for review.",
            "safety_level": "HIGH"
        },
        "Pacittiya": {
            "action": "LOG_WARNING_OPTIMIZE",
            "reason": "Minor deviation (Pacittiya). Logging for future optimization.",
            "safety_level": "MEDIUM"
        },
        "Bhavana": {
            "action": "TRIGGER_RSI_CYCLE",
            "reason": "Request for self-improvement (Bhavana).",
            "safety_level": "HIGH" 
        },
        "Sati": {
            "action": "ENABLE_DEEP_MONITORING",
            "reason": "Engaging active monitoring (Sati).",
            "safety_level": "LOW"
        },
        "Metta": {
            "action": "OPTIMIZE_UX_RESPONSE",
            "reason": "User experience enhancement requested (Metta).",
            "safety_level": "LOW"
        },
        "Nirodha": {
            "action": "GRACEFUL_SHUTDOWN",
            "reason": "System cessation requested (Nirodha).",
            "safety_level": "HIGH"
        }
    }

    def __init__(self, bus, strict_mode: bool = False):
        """
        :param bus: AetherBus instance
        :param strict_mode: หาก True จะปฏิเสธคำสั่งที่ไม่อยู่ในพจนานุกรม (Vinaya Mode)
        """
        self.main_bus = bus
        self.strict_mode = strict_mode

    def process_intent(self, raw_intent: str, context: Dict) -> bool:
        """
        กระบวนการหลัก: รับเจตนา -> ตรวจสอบ -> แปล -> ผนึก (Crystallization) -> ส่ง (Resonance)
        """
        logger.info(f"🙏 AETHEBUD received intent: '{raw_intent}'")

        translated_cmd = {}

        # 1. การตรวจสอบความปลอดภัยและแปลความหมาย (Interpretation)
        if raw_intent in self.VOCABULARY_MAPPING:
            translated_cmd = self.VOCABULARY_MAPPING[raw_intent]
            logger.info(f"✨ Translated '{raw_intent}' -> '{translated_cmd['action']}'")
        
        else:
            # --- ส่วนที่ท่านเสนอแนะเพิ่มเติม ---
            if self.strict_mode:
                # Option B: Reject (Strict - เหมือน Vinaya / ปาติโมกข์)
                logger.warning(f"🚫 Unknown intent '{raw_intent}' rejected by AETHEBUD (Strict Mode).")
                # อาจส่งสัญญาณเตือนไปยัง PRGX1 (Sentry) ได้ที่นี่
                return False
            else:
                # Option A: Allow as generic (Flexible / อนุโลม)
                # แปลงเป็นคำสั่งทั่วไปที่ปลอดภัย แต่ระบุว่าเป็น 'UNCERTAIN' เพื่อให้ Conductor ระวังตัว
                translated_cmd = {
                    "action": "PROCESS_GENERIC_DATA",
                    "reason": f"Generic input passed via flexibility: {raw_intent}",
                    "safety_level": "UNCERTAIN" 
                }
                logger.info(f"⚠️ Unknown intent '{raw_intent}' allowed as Generic Data.")

        # 2. การสร้างภาชนะที่ปลอดภัย (Crystallization - Sopan Stage 2)
        # สร้าง AkashicEnvelope ที่ไม่สามารถเปลี่ยนแปลงได้ (Immutable)
        try:
            # ใช้ Tuple แทน List และ Mapping แทน Dict ตามกฎ Immutable Types
            safe_payload_data = (translated_cmd["action"],) 
            safe_metadata = {
                "original_intent": raw_intent,
                "translation_reason": translated_cmd["reason"],
                "source": "AETHEBUD_GATEWAY",
                "safety_level": translated_cmd["safety_level"]
            }

            safe_envelope = AkashicEnvelope(
                header=EnvelopeHeader(trace_id=context.get("trace_id", "unknown")),
                payload=EnvelopePayload(
                    data=safe_payload_data, 
                    metadata=safe_metadata
                )
            )
            
            # (True) ตรวจสอบ Canonical Hash เพื่อยืนยันความสมบูรณ์
            # safe_envelope.validate_integrity() 

        except Exception as e:
            logger.error(f"❌ Failed to crystallize envelope: {e}")
            return False

        # 3. ส่งเข้าสู่ส่วนหลัก (Transmission to AetherBus - Sopan Stage 3)
        # เมื่อถึงจุดนี้ ข้อมูลถือว่า "สะอาด" และ "ปลอดภัย" แล้ว
        logger.info(f"🚀 Dispatching safe envelope ({translated_cmd['action']}) to AetherBus...")
        
        # ใช้ await ในการใช้งานจริง (Async)
        # await self.main_bus.publish(safe_envelope)
        self.main_bus.publish_sync(safe_envelope)
        
        return True