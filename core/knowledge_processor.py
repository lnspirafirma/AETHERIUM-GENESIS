import asyncio
from typing import List, Dict, Any, Optional
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
    เปลี่ยนจากการ Search หาคำตอบ เป็นการ 'สังเคราะห์' คำตอบจากความขัดแย้ง
    """

    def __init__(self, graph_db: SimpleKnowledgeGraph, vector_db: SimpleVectorDB):
        self.graph_db = graph_db
        self.vector_db = vector_db

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

        for node in nodes:
            # Query Graph Database: "Find nodes linked by 'conflicts_with' edge"
            conflict_ids = self.graph_db.get_related_ids(node.id, relation_type="conflicts_with")

            for cid in conflict_ids:
                if cid not in seen_ids:
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
