import asyncio
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from core.knowledge_base import KnowledgeNode, SimpleKnowledgeGraph

class SimpleVectorDB:
    """
    Mock Vector Database อย่างง่ายสำหรับการค้นหา Similarity
    """
    def __init__(self, graph: SimpleKnowledgeGraph):
        self.graph = graph

    async def search(self, query: str, top_k: int = 1) -> List[KnowledgeNode]:
        """
        Mock Search Logic: ค้นหา Node จาก Keyword ใน Query
        (ใน Production จริง จะใช้ Cosine Similarity)
        """
        results = []
        query_lower = query.lower()

        # Simple Keyword Matching for Simulation
        for node in self.graph.nodes.values():
            # ถ้าเจอ keyword ที่ตรงกับเนื้อหา (mock logic)
            if "profit" in query_lower and "profit" in node.content.lower():
                results.append(node)
            elif "ethic" in query_lower and "ethic" in node.content.lower():
                results.append(node)
            elif "sky" in query_lower and "sky" in node.content.lower():
                results.append(node)
            elif "stability" in query_lower and "stability" in node.content.lower():
                results.append(node)
            # Legacy/Generic match for other keywords to ensure tests pass
            elif any(word in node.content.lower() for word in query_lower.split() if len(word) > 3):
                 results.append(node)

        # Fallback: ถ้าไม่เจออะไรเลย ให้คืนค่าว่าง หรือค่า default (ถ้าจำเป็น)
        # De-duplicate results
        seen = set()
        unique_results = []
        for r in results:
            if r.id not in seen:
                unique_results.append(r)
                seen.add(r.id)

        return unique_results[:top_k]

    def get_by_ids(self, ids: List[str]) -> List[KnowledgeNode]:
        """ดึงข้อมูล Node หลายตัวจาก ID"""
        return [self.graph.get_node(i) for i in ids if self.graph.get_node(i)]


class KnowledgeCentricProcessor:
    """
    KCP (Panya Engine):
    Combines Dialectical Thinking with RAG/Memory Bank capabilities.
    """

    def __init__(self, graph_db: Optional[SimpleKnowledgeGraph] = None, vector_db: Optional[SimpleVectorDB] = None, embedding_dim=512):
        self.graph_db = graph_db or SimpleKnowledgeGraph()
        self.vector_db = vector_db or SimpleVectorDB(self.graph_db)

        # --- RAG / MindLogic Components ---
        self.knowledge_base: Dict[str, np.ndarray] = {} # Key -> Embedding
        self.history_log: List[str] = []
        self.embedding_dim = embedding_dim

    # --- Dialectical Methods (Original KCP) ---
    async def synthesize_wisdom(self, query: str) -> str:
        """
        The Dialectical Loop: Thesis -> Antithesis -> Synthesis
        """
        # 1. Thesis: หาข้อมูลที่ตรงกับคำถาม (Similarity Search)
        thesis_nodes = await self.vector_db.search(query, top_k=3)

        if not thesis_nodes:
            return "No relevant knowledge found to synthesize."

        # 2. Antithesis: หาข้อมูลที่ 'ขัดแย้ง' หรือ 'ท้าทาย' ข้อมูลชุดแรก
        # (ใช้ Graph Edge 'conflicts_with')
        antithesis_nodes = await self._find_contradictions(thesis_nodes)

        # 3. Construct Prompt (Synthesis)
        # หากไม่มี Antithesis ก็จะคืนค่า Thesis ปกติ
        result_prompt = self._construct_dialectical_prompt(
            query, thesis_nodes, antithesis_nodes
        )

        return result_prompt

    async def _find_contradictions(self, nodes: List[KnowledgeNode]) -> List[KnowledgeNode]:
        """
        ค้นหา Shadow Node (คู่ขัดแย้ง) จาก Graph Memory
        """
        contradictions = []
        seen_ids = set()

        # Create a set of input node IDs to prevent overlapping with Thesis
        thesis_ids = {n.id for n in nodes}

        for node in nodes:
            # Query Graph Database: "Find nodes linked by 'conflicts_with' edge"
            conflict_ids = self.graph_db.get_related_ids(node.id, relation_type="conflicts_with")

            for cid in conflict_ids:
                if cid not in seen_ids and cid not in thesis_ids:
                    # ดึงข้อมูล Node เต็มจาก ID
                    conflict_node = self.graph_db.get_node(cid)
                    if conflict_node:
                        contradictions.append(conflict_node)
                        seen_ids.add(cid)

        return contradictions

    def _construct_dialectical_prompt(self, query: str, thesis: List[KnowledgeNode], antithesis: List[KnowledgeNode]) -> str:
        """สร้างข้อความ Prompt เพื่อส่งให้ AI สังเคราะห์"""

        def extract_text(nodes):
            return "\n".join([f"- {n.content}" for n in nodes])

        thesis_text = extract_text(thesis)

        # กรณีไม่มีความขัดแย้ง (Knowledge Retrieval ปกติ)
        if not antithesis:
            return (
                f"QUERY: {query}\n"
                f"RELEVANT KNOWLEDGE:\n{thesis_text}\n"
                f"INSTRUCTION: Answer based on the knowledge above."
            )

        # กรณีมีความขัดแย้ง (Dialectical Synthesis)
        antithesis_text = extract_text(antithesis)

        return (
            f"QUERY: {query}\n\n"
            f"--- PERSPECTIVE A (Thesis) ---\n"
            f"{thesis_text}\n\n"
            f"--- PERSPECTIVE B (Antithesis/Challenge) ---\n"
            f"{antithesis_text}\n\n"
            f"--- SYNTHESIS TASK ---\n"
            f"Analyze the tension between A and B. "
            f"Do not just summarize. "
            f"Create a new insight (Synthesis) that resolves this paradox "
            f"aligning with Constructive Evolution."
        )

    # --- RAG / Embedding Methods (MindLogic Enhancements) ---

    def _generate_embedding(self, text: str) -> np.ndarray:
        """ สร้าง Embedding Vector จำลอง (512-dim) """
        np.random.seed(hash(text) % 2**32)
        return np.random.rand(self.embedding_dim)

    def get_embedding_with_fallback(self, data_input: str) -> Dict:
        """ จำลองการดึง Embedding พร้อม Fallback Logic """
        # Simplified: Always succeed for simulation
        vector = self._generate_embedding(data_input)
        return {'vector': vector, 'source': 'Core_Model', 'dim': len(vector)}

    def add_knowledge(self, data_input: str, embedding: np.ndarray, source: str, dim: int):
        """
        ประมวลผลและจัดเก็บ Input เป็นความรู้ใหม่ลง Memory Bank
        """
        if data_input in self.knowledge_base:
            return

        self.knowledge_base[data_input] = embedding
        self.history_log.append(f"Added: '{data_input}' from {source} (Dim: {dim})")

    def rag_retrieve(self, current_embedding: np.ndarray) -> Tuple[str, float]:
        """ จำลองการดึงความรู้ที่ใกล้เคียงที่สุดจาก Memory Bank (RAG) """
        if not self.knowledge_base:
            return "The Void", 0.0

        best_key = ""
        max_sim = -1.0

        for key, vector in self.knowledge_base.items():
            # Calculate Cosine Similarity
            # Ensure vectors are same dimension, trim if needed
            k_vec = vector[:self.embedding_dim]
            c_vec = current_embedding[:self.embedding_dim]

            similarity = np.dot(c_vec, k_vec) / (np.linalg.norm(c_vec) * np.linalg.norm(k_vec))

            if similarity > max_sim:
                max_sim = similarity
                best_key = key

        return best_key, float(max_sim) if max_sim > 0 else 0.0
