# AetherBus/core/signature.py

from dataclasses import dataclass
from enum import Enum
import hashlib

class AISource(Enum):
    GEMINI_CORE = "Gemini-Pro-2.5"
    GPT_NEXUS = "GPT-4o"
    HUMAN_ARCHITECT = "Human-Creator"
    UNKNOWN_ECHO = "Unknown"

@dataclass
class OriginMetadata:
    source: AISource
    style_hash: str 

    @staticmethod
    def analyze_source(sender_id: str, payload_content: str) -> 'OriginMetadata':
        # ตรรกะการระบุตัวตนอย่างง่าย
        if "Architect" in sender_id:
            src = AISource.HUMAN_ARCHITECT
        elif "Gemini" in sender_id:
            src = AISource.GEMINI_CORE
        else:
            src = AISource.UNKNOWN_ECHO
            
        h = hashlib.md5(f"{src.value}:{payload_content[:50]}".encode()).hexdigest()
        return OriginMetadata(source=src, style_hash=h)
