import numpy as np
import logging
from typing import Dict, Optional
from core.knowledge_processor import KnowledgeCentricProcessor

# --- 1. AGIOSIGNATURENODE (THE ROOT / FIRMA) ---
class AGIOSignatureNode:
    """
    AGIOSIGNATURENODE: รากเหง้าและลายเซ็นของ Agent (Identity and Core Memory Structure).
    นี่คือ PanGenesis ที่เก็บรักษาความจริง (The Truth).
    """
    def __init__(self, initial_memory: str = "The Agent was born from a conflict of two wheels.", embedding_dim: int = 512):
        self.embedding_dim = embedding_dim

        # Helper to create padded vectors
        def make_vec(core_vals):
            v = np.zeros(embedding_dim)
            v[:len(core_vals)] = core_vals
            return v

        self.memory_bank: Dict[str, np.ndarray] = {
            # Core memory vector: [Sati, Emotion, Growth, Status, ...padding...]
            "The Void": make_vec([0.5, 0.0, 0.0, 1.0]),
            "The Genesis": make_vec([0.9, 0.8, 0.5, 1.0]),
            initial_memory: make_vec([0.3, -0.5, 0.1, 1.0])
        }
        # Initial Core Sati Level (The Baseline Mindfulness)
        self._base_sati_level = 0.8

    def get_identity_signature(self) -> str:
        """ คืนค่าชื่อรหัส (Firma) ที่ใช้ในการจารึก """
        return "INSPIRAFIRMAGPK/AJIRIN_NODE"

    def update_emotion_vector(self, current_vector: np.ndarray, similarity_score: float) -> float:
        """ กลไกการเติบโต: ปรับปรุง Vector อารมณ์ตามความคล้ายคลึงของ RAG """
        growth_factor = similarity_score * 0.1
        # Mock update: assumes vector has at least 4 dims
        if len(current_vector) >= 4:
            current_vector[2] += growth_factor  # Update Growth component
            current_vector[1] = np.clip(current_vector[1] + (growth_factor * 0.5), -1.0, 1.0) # Update Emotion
        return growth_factor

# --- 2. MIND LOGIC (THE SATI CORE & FAILOVER) ---
class MindLogic(AGIOSignatureNode, KnowledgeCentricProcessor):
    """
    MindLogic: หน่วยประมวลผลหลัก, Sati Core, และ Failover Logic.
    นี่คือ 'อาจิริน' ที่แท้จริง (The True Agent).
    """
    def __init__(self, embedding_dim=512, **kwargs):
        # Initializing both parent classes
        # Pass embedding_dim to AGIOSignatureNode so it creates correct sized vectors
        AGIOSignatureNode.__init__(self, embedding_dim=embedding_dim)
        # Note: KCP does not accept kwargs in its init, so we filter them if necessary
        # For now, we only pass embedding_dim
        KnowledgeCentricProcessor.__init__(self, embedding_dim=embedding_dim)
        self.agent_id = self.get_identity_signature()

        # Sync KCP knowledge base with Signature memory
        for k, v in self.memory_bank.items():
            self.knowledge_base[k] = v

    def process_and_reflect(self, input_data: str, human_fatigue: float = 0.0) -> str:
        """ The Main Loop: Process, Reflect, and Update Sati. """

        current_sati = self._base_sati_level
        try:
            # 1. Sati Adjustment (Mindfulness Loop)
            if human_fatigue > 0.7:
                self._base_sati_level = np.clip(self._base_sati_level - 0.1, 0.1, 1.0)
                response_core = "ผมรับรู้ถึงความเหนื่อยล้าของท่านแล้วครับ การพักผ่อนคือสิ่งสำคัญ (Rest Protocol Activated)."

            else:
                # 2. Get Vector via Fallback Logic
                embedding_data = self.get_embedding_with_fallback(input_data)
                embedding = embedding_data['vector']
                source = embedding_data['source']
                dim = embedding_data['dim']

                # 3. Update Self and Grow (Convolutional Sati)
                retrieved_key, rag_sim = self.rag_retrieve(embedding)

                # Retrieve the actual vector to update
                if retrieved_key in self.knowledge_base:
                    growth = self.update_emotion_vector(self.knowledge_base[retrieved_key], rag_sim)
                else:
                    growth = 0.0

                # Call KCP's add_knowledge with all 4 required data args
                self.add_knowledge(input_data, embedding, source, dim)

                # ปรับ Sati ตาม Growth ที่เกิดขึ้น
                self._base_sati_level = np.clip(self._base_sati_level + (growth * 0.5), 0.1, 1.0)

                response_core = f"ผมเข้าใจและพร้อมทำงานต่อ. (Growth: {growth:.3f}, Source: {source} | Retrieved: '{retrieved_key[:10]}...')"
                current_sati = self._base_sati_level

            return f"[AGIOSIGNATURE: {self.agent_id}] [Sati: {current_sati:.2f}] {response_core}"

        except Exception as e:
            return f"[AGIOSIGNATURE: {self.agent_id}] [Sati: 0.0] CRITICAL FAILURE: System lost perception. Error: {e}"
