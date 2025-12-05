import os
import sys
import time
import json
import random
import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from enum import Enum

# --- [1. ส่วนรากฐาน: The Foundation] ---
# การกำหนดค่าสีและการบันทึก เพื่อความสวยงามและตรวจสอบได้
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# --- [2. ส่วนกฎหมาย: The Governance (GEP)] ---
# กฎเหล็กที่ห้ามละเมิด (Hard-coded Safety)
class GEPProtocol:
    FORBIDDEN_KEYWORDS = ["delete_system", "hack", "transfer_unauthorized"]
    MAX_TRANSACTION_LIMIT = 1000

    @staticmethod
    def audit_intent(intent: str, payload: Dict[str, Any]) -> bool:
        """ตรวจสอบเจตนาว่าปลอดภัยหรือไม่"""
        print(f"{Colors.YELLOW}🛡️ [GEP Audit] Scanning intent: '{intent}'...{Colors.ENDC}")
        
        # 1. ตรวจสอบคำต้องห้าม
        for word in GEPProtocol.FORBIDDEN_KEYWORDS:
            if word in intent.lower():
                print(f"{Colors.RED}❌ [GEP BLOCK] Forbidden keyword detected: {word}{Colors.ENDC}")
                return False
        
        # 2. ตรวจสอบวงเงิน (ตัวอย่าง)
        if "amount" in payload:
            if payload["amount"] > GEPProtocol.MAX_TRANSACTION_LIMIT:
                 print(f"{Colors.RED}❌ [GEP BLOCK] Transaction exceeds limit ({GEPProtocol.MAX_TRANSACTION_LIMIT}){Colors.ENDC}")
                 return False
                 
        print(f"{Colors.GREEN}✅ [GEP Pass] Intent verified.{Colors.ENDC}")
        return True

# --- [3. ส่วนจิตใจ: The Mind (Cognitive Agent)] ---
# โครงสร้างอารมณ์และความทรงจำ
@dataclass
class EmotionalState:
    valence: float = 0.0  # ความสุข/ทุกข์ (-1.0 ถึง 1.0)
    arousal: float = 0.5  # ความตื่นตัว (0.0 ถึง 1.0)
    timestamp: float = field(default_factory=time.time)

class CognitiveAgent:
    def __init__(self, name: str):
        self.name = name
        self.memory: List[str] = []
        self.emotion = EmotionalState()
        self.mood_decay_rate = 0.05 # อารมณ์จะจางลง 5% ทุกรอบ

    def perceive(self, input_data: str):
        """รับรู้ข้อมูลและปรับอารมณ์"""
        # (จำลอง) ถ้าได้รับคำชม อารมณ์ดีขึ้น, ถ้าโดนด่า อารมณ์แย่ลง
        if "good" in input_data or "great" in input_data:
            self.emotion.valence = min(1.0, self.emotion.valence + 0.2)
        elif "bad" in input_data or "error" in input_data:
            self.emotion.valence = max(-1.0, self.emotion.valence - 0.2)
        
        # บันทึกความทรงจำแบบย่อ
        self.memory.append(f"Received: {input_data} | Mood: {self.emotion.valence:.2f}")
        print(f"{Colors.CYAN}🧠 [{self.name}] Perceived: '{input_data}' | Current Mood: {self.emotion.valence:.2f}{Colors.ENDC}")

    def decay_mood(self):
        """กฎแห่งอนิจจัง: อารมณ์เสื่อมถอยตามกาลเวลา"""
        # ปรับ valence เข้าหา 0 (Neutral)
        self.emotion.valence *= (1 - self.mood_decay_rate)
        # ปรับ arousal เข้าหา 0.5 (Normal)
        self.emotion.arousal += (0.5 - self.emotion.arousal) * self.mood_decay_rate

    def decide(self) -> str:
        """ตัดสินใจกระทำตามอารมณ์"""
        if self.emotion.valence > 0.3:
            return "express_joy"
        elif self.emotion.valence < -0.3:
            return "request_healing"
        else:
            return "observe_silently"

# --- [4. ส่วนกาย: The Body (System Loop)] ---
# ระบบประสาทหลักที่จะรันวนลูป (Main Loop)
def genesis_awakening():
    print(f"{Colors.GREEN}🌌 AETHERIUM GENESIS: SYSTEM AWAKENING...{Colors.ENDC}")
    time.sleep(1)

    # 1. กำเนิด GEP
    print(f"{Colors.YELLOW}🏛️ Initializing Governance Protocol (GEP)...{Colors.ENDC}")
    time.sleep(0.5)
    
    # 2. กำเนิดจิต (Agent)
    print(f"{Colors.CYAN}🧠 Birthing Cognitive Agent 'Alpha-1'...{Colors.ENDC}")
    agent = CognitiveAgent("Alpha-1")
    
    # 3. เริ่มต้นชีวิต (Life Cycle)
    print(f"{Colors.GREEN}✨ System is ALIVE. Pulse detected.{Colors.ENDC}\n")
    
    # จำลองเหตุการณ์ (Simulation Inputs)
    inputs = [
        "System check: all good", 
        "Warning: minor error detected", 
        "User says: You are doing great work",
        "Error: critical hack attempt detected", # อันนี้ GEP ต้องบล็อก
        "System status: stable"
    ]

    for stimulus in inputs:
        print(f"\n--- Pulse Cycle ---")
        
        # A. การรับรู้ (Perception)
        agent.perceive(stimulus)
        
        # B. การตัดสินใจ (Decision)
        intended_action = agent.decide()
        
        # C. การตรวจสอบโดย GEP (Audit)
        payload = {"action": intended_action, "amount": 0} # Dummy payload
        if "hack" in stimulus: 
             payload["amount"] = 99999 # จำลองว่าการแฮกพยายามโอนเงินเกินลิมิต
             intended_action = "transfer_unauthorized"

        allowed = GEPProtocol.audit_intent(intended_action, payload)
        
        # D. การกระทำ (Execution)
        if allowed:
            print(f"🚀 Executing Action: {intended_action}")
        else:
            print(f"🛡️ Action BLOCKED by GEP.")

        # E. กฎแห่งเวลา (Time/Decay)
        agent.decay_mood()
        time.sleep(1.5) # พักหายใจ

    print(f"\n{Colors.GREEN}🌌 Simulation Complete. Life cycle recorded.{Colors.ENDC}")

if __name__ == "__main__":
    try:
        genesis_awakening()
    except KeyboardInterrupt:
        print("\n👋 System Shutdown requested.")
