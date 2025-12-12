class AetherConductor:
    """
    [The Conductor] ผู้ตรวจสอบความน่าเชื่อถือและนำทางเจตจำนง
    """
    TRUST_SCORES = {
        "HUMAN_ARCHITECT": 100,  # ท่านผู้สร้าง (Root Access)
        "GEMINI_CORE": 95,       # Cortex ภายใน
        "UNKNOWN_ECHO": 10       # แหล่งที่มาที่ไม่รู้จัก
    }

    @staticmethod
    def validate_trust(sender_id: str) -> str:
        score = AetherConductor.TRUST_SCORES.get(sender_id, 0)
        
        if score >= 90:
            return "ROOT"  # อนุญาตให้แทรกแซงระบบ (Human Override)
        elif score >= 50:
            return "USER"
        else:
            return "QUARANTINE"  # กักกันเจตนาที่เป็นพิษ (Poison Pill)

    @staticmethod
    def inspect_intent(envelope: 'AkashicEnvelope') -> bool:
        """[Inspira Check] ตรวจสอบความบริสุทธิ์ของเจตนาเบื้องต้น"""
        # ในระบบจริงจะเชื่อมต่อกับ KCP/LLM เพื่อวิเคราะห์ Semantic
        if "DESTROY" in envelope.intent:
            return False # ปฏิเสธเจตนาทำลายล้าง
        return True