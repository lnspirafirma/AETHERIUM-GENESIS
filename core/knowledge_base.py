from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class KnowledgeNode:
    """
    หน่วยย่อยที่สุดของความรู้ (The Atom of Wisdom)
    """
    id: str
    content: str
    vector: Optional[List[float]] = field(default=None) # Mock vector embedding
    metadata: Dict[str, Any] = field(default_factory=dict)

class SimpleKnowledgeGraph:
    """
    จำลอง Graph Database ด้วย Adjacency List (Dictionary)
    Structure: { source_id: { relation_type: [target_id, ...] } }
    """
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: Dict[str, Dict[str, List[str]]] = {}

    def add_node(self, node: KnowledgeNode):
        self.nodes[node.id] = node

    def add_edge(self, source_id: str, relation: str, target_id: str):
        """สร้างความเชื่อมโยงระหว่างข้อมูล (Subject -> Predicate -> Object)"""
        if source_id not in self.edges:
            self.edges[source_id] = {}

        if relation not in self.edges[source_id]:
            self.edges[source_id][relation] = []

        if target_id not in self.edges[source_id][relation]:
            self.edges[source_id][relation].append(target_id)

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        return self.nodes.get(node_id)

    def get_related_ids(self, node_id: str, relation_type: str) -> List[str]:
        """ค้นหา Node ปลายทางตามประเภทความสัมพันธ์"""
        # print(f"DEBUG: get_related_ids id={node_id} rel={relation_type}")
        # print(f"DEBUG: Current Edges: {self.edges}")
        if node_id in self.edges and relation_type in self.edges[node_id]:
            return self.edges[node_id][relation_type]
        return []

    # Helper method เพื่อ Load Mock Data สำหรับทดสอบ
    def load_mock_data(self):
        # Thesis: Profit Focus
        n1 = KnowledgeNode(id="A1", content="Maximize efficiency and profit at all costs.", vector=[0.9, 0.1])
        # Antithesis: Ethics Focus (Conflicts with A1)
        n2 = KnowledgeNode(id="B1", content="Prioritize ethical art and human well-being over metrics.", vector=[0.1, 0.9])

        # Neutral Facts
        n3 = KnowledgeNode(id="C1", content="The sky is blue.", vector=[0.5, 0.5])

        # Additional Context for Stability Check (Legacy Support)
        n4 = KnowledgeNode(id="S1", content="System Stability is crucial.", vector=[0.5, 0.5])

        self.add_node(n1)
        self.add_node(n2)
        self.add_node(n3)
        self.add_node(n4)

        # Define Logic: A1 conflicts with B1
        self.add_edge("A1", "conflicts_with", "B1")
        self.add_edge("B1", "conflicts_with", "A1")
