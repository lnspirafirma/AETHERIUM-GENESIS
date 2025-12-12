import logging
from typing import Dict, Optional, Tuple, Any

# ******************************************************************************
# แก้ไขไวยากรณ์: ลบเครื่องหมาย ',' ที่เกินมา และลบบรรทัด import ที่ไม่ถูกต้อง
# ******************************************************************************
from aetherium.envelope.models import AkashicEnvelope, EnvelopeHeader, EnvelopePayload

# จำลอง AetherBus พื้นฐานสำหรับการใช้งานแบบ Synchronous
class MockAetherBus:
    """Mock/Stub สำหรับ AetherBus เพื่อให้ AetheBudGuard รันได้"""
    def publish_sync(self, envelope: AkashicEnvelope):
        """จำลองการส่งข้อมูลแบบ Synchronous"""
        logger.debug(f"AetherBus: Published Envelope with Action: {envelope.payload.metadata.get('translation_reason')}")
        # ในการใช้งานจริง: อาจจะมีการเรียกใช้ระบบอื่นๆ ต่อไป

logger = logging.getLogger("AETHEBUD")

class AetheBudGuard:
    """
    ผู้แปลเจตนา (Intent Translator) และผู้รักษาประตู (Gatekeeper)
    ทำหน้าที่แปลงภาษา 'AETHEBUD' ให้เป็น 'Technical Safe Terms' 
    เพื่อป้องกันการถูกบล็อกจาก Semantic Firewall ภายนอก (Sopan Stage 1)
    """

    # พจนานุกรมแปลภาษา AETHEBUD -> Technical Safe Terms (ฉบับขยาย)
    VOCABULARY_MAPPING: Dict[str, Dict[str, Any]] = {
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

    def __init__(self, bus: 'MockAetherBus', strict_mode: bool = False):
        """
        :param bus: AetherBus instance (หรือ MockAetherBus สำหรับการทดสอบ)
        :param strict_mode: หาก True จะปฏิเสธคำสั่งที่ไม่อยู่ในพจนานุกรม (Vinaya Mode)
        """
        if not hasattr(bus, 'publish_sync'):
             raise TypeError("Bus instance must have a 'publish_sync' method.")
             
        self.main_bus = bus
        self.strict_mode = strict_mode
        logger.info(f"AetheBudGuard initialized. Strict Mode: {self.strict_mode}")


    def process_intent(self, raw_intent: str, context: Dict) -> bool:
        """
        กระบวนการหลัก: รับเจตนา -> ตรวจสอบ -> แปล -> ผนึก (Crystallization) -> ส่ง (Resonance)
        
        Args:
            raw_intent (str): เจตนา/คำสั่งดิบที่เข้ามา
            context (Dict): ข้อมูลบริบท เช่น trace_id
            
        Returns:
            bool: True หากกระบวนการเสร็จสมบูรณ์, False หากเกิดข้อผิดพลาดหรือถูกปฏิเสธ
        """
        logger.info(f"🙏 AETHEBUD received intent: '{raw_intent}'")

        translated_cmd: Dict[str, str] = {}
        
        # 1. การตรวจสอบความปลอดภัยและแปลความหมาย (Interpretation)
        if raw_intent in self.VOCABULARY_MAPPING:
            # ใช้ .copy() เพื่อป้องกันการเปลี่ยนแปลงค่าใน VOCABULARY_MAPPING
            translated_cmd = self.VOCABULARY_MAPPING[raw_intent].copy() 
            logger.info(f"✨ Translated '{raw_intent}' -> '{translated_cmd['action']}'")

        else:
            if self.strict_mode:
                # Option B: Reject (Strict - Vinaya Mode)
                logger.warning(f"🚫 Unknown intent '{raw_intent}' rejected by AETHEBUD (Strict Mode).")
                return False
            else:
                # Option A: Allow as generic (Flexible Mode)
                translated_cmd = {
                    "action": "PROCESS_GENERIC_DATA",
                    "reason": f"Generic input passed via flexibility: {raw_intent}",
                    "safety_level": "UNCERTAIN" 
                }
                logger.info(f"⚠️ Unknown intent '{raw_intent}' allowed as Generic Data.")

        # 2. การสร้างภาชนะที่ปลอดภัย (Crystallization - Sopan Stage 2)
        try:
            # ใช้ Tuple สำหรับ data เพื่อความเป็น Immutable
            safe_payload_data = (translated_cmd["action"],) 
            safe_metadata = {
                "original_intent": raw_intent,
                "translation_reason": translated_cmd["reason"],
                "source": "AETHEBUD_GATEWAY",
                "safety_level": translated_cmd["safety_level"]
            }

            # สร้าง Header โดยใช้ trace_id จาก context
            header = EnvelopeHeader(trace_id=context.get("trace_id", "unknown"))
            
            # สร้าง Payload
            payload = EnvelopePayload(
                data=safe_payload_data, 
                metadata=safe_metadata
            )
            
            # สร้าง Akashic Envelope ที่สมบูรณ์
            safe_envelope = AkashicEnvelope(
                header=header,
                payload=payload
            )

        except Exception as e:
            logger.error(f"❌ Failed to crystallize envelope for '{raw_intent}': {e}", exc_info=True)
            return False

        # 3. ส่งเข้าสู่ส่วนหลัก (Transmission to AetherBus - Sopan Stage 3)
        logger.info(f"🚀 Dispatching safe envelope ({translated_cmd['action']}) to AetherBus...")

        try:
            self.main_bus.publish_sync(safe_envelope)
        except Exception as e:
            logger.error(f"❌ Failed to publish envelope to AetherBus: {e}", exc_info=True)
            return False

        return True
    
# ******************************************************************************
# โค้ดตัวอย่างการใช้งาน
# ******************************************************************************
if __name__ == "__main__":
    # ตั้งค่า Logging สำหรับการแสดงผล
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # จำลองส่วนประกอบที่ต้องใช้
    mock_bus = MockAetherBus()
    context_data = {"trace_id": "AETHE-TEST-123"}

    print("\n--- TEST: Strict Mode (Vinaya Mode) ---")
    guard_strict = AetheBudGuard(bus=mock_bus, strict_mode=True)
    
    # 1. คำสั่งที่รู้จัก (Metta)
    guard_strict.process_intent("Metta", context_data)
    
    # 2. คำสั่งที่ไม่รู้จัก (Unknown_Action) -> ถูกปฏิเสธ
    guard_strict.process_intent("Unknown_Action", context_data) 
    
    print("\n--- TEST: Flexible Mode (Default) ---")
    guard_flexible = AetheBudGuard(bus=mock_bus, strict_mode=False) 

    # 3. คำสั่งที่ไม่รู้จัก (Anicca) -> อนุญาตให้ผ่านเป็น Generic
    guard_flexible.process_intent("Anicca", context_data)
    
    # 4. คำสั่ง Parajika -> HALT
    guard_flexible.process_intent("Parajika", {"trace_id": "AETHE-CRITICAL-456"})
    
    print("\n--- End of AetheBudGuard Test ---")