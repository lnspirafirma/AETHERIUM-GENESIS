from dataclasses import dataclass
from enum import Enum
import hashlib
import time

class AISource(Enum):
    GEMINI_CORE = "Gemini-Pro-2.5"
    GPT_NEXUS = "GPT-4o"
    CLAUDE_SONNET = "Claude-3.5"
    HUMAN_ARCHITECT = "Human-Creator"
    UNKNOWN_ECHO = "Unknown"

@dataclass
class OriginMetadata:
    source: AISource
    style_hash: str

    @staticmethod
    def analyze_code_style(content_str: str) -> 'OriginMetadata':
        if "AGIO-CODEX" in content_str or "gep_constitution" in content_str:
            src = AISource.GEMINI_CORE
        elif "Architect" in content_str:
            src = AISource.HUMAN_ARCHITECT
        else:
            src = AISource.UNKNOWN_ECHO

        h = hashlib.md5(f"{src.value}:{content_str[:50]}".encode()).hexdigest()
        return OriginMetadata(source=src, style_hash=h)
