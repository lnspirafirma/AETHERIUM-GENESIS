import pytest
from core.knowledge_base import SimpleKnowledgeGraph, KnowledgeNode
from core.knowledge_processor import KnowledgeCentricProcessor

@pytest.mark.asyncio
async def test_kcp_thesis_antithesis_no_overlap():
    graph = SimpleKnowledgeGraph()
    # A1 conflicts with B1
    n1 = KnowledgeNode(id="A1", content="Profit", vector=[])
    n2 = KnowledgeNode(id="B1", content="Ethics", vector=[])
    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_edge("A1", "conflicts_with", "B1")
    graph.add_edge("B1", "conflicts_with", "A1")

    # Mock vector db to return both A1 and B1
    class MockVectorDB:
        def __init__(self, graph): self.graph = graph
        async def search(self, query, top_k=1):
            return [n1, n2]

    vector_db = MockVectorDB(graph)
    kcp = KnowledgeCentricProcessor(graph, vector_db)

    # Calling internal method directly or via synthesize_wisdom
    thesis_nodes = await vector_db.search("query")
    antithesis_nodes = await kcp._find_contradictions(thesis_nodes)

    # Assert that no node in antithesis_nodes is present in thesis_nodes
    thesis_ids = {n.id for n in thesis_nodes}
    for anode in antithesis_nodes:
        assert anode.id not in thesis_ids, f"Node {anode.id} found in both Thesis and Antithesis"

    # In this specific case, since A1 and B1 conflict with each other and both are in Thesis,
    # Antithesis should be empty.
    assert len(antithesis_nodes) == 0
