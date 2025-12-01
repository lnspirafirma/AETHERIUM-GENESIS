import pytest
from core.knowledge_base import SimpleKnowledgeGraph, KnowledgeNode
from core.knowledge_processor import KnowledgeCentricProcessor, SimpleVectorDB

@pytest.fixture
def kcp():
    graph = SimpleKnowledgeGraph()
    graph.load_mock_data()
    vector_db = SimpleVectorDB(graph)
    return KnowledgeCentricProcessor(graph, vector_db)

@pytest.mark.asyncio
async def test_kcp_thesis_only(kcp):
    # Query "sky" matches C1 ("The sky is blue.")
    wisdom = await kcp.synthesize_wisdom("sky")
    assert "The sky is blue" in wisdom
    assert "SYNTHESIS TASK" not in wisdom

@pytest.mark.asyncio
async def test_kcp_dialectical_synthesis(kcp):
    wisdom = await kcp.synthesize_wisdom("maximize profit")
    assert "PERSPECTIVE A (Thesis)" in wisdom
    assert "PERSPECTIVE B (Antithesis/Challenge)" in wisdom
    assert "SYNTHESIS TASK" in wisdom

@pytest.mark.asyncio
async def test_kcp_no_knowledge(kcp):
    wisdom = await kcp.synthesize_wisdom("Unrelated nonsense")
    assert "No relevant knowledge" in wisdom

@pytest.mark.asyncio
async def test_kcp_stability_check(kcp):
    # Tests the specific "stability" keyword logic in SimpleVectorDB
    wisdom = await kcp.synthesize_wisdom("Check system stability")
    assert "Stability is crucial" in wisdom

@pytest.mark.asyncio
async def test_kcp_fallback_match(kcp):
    # Tests the fallback 'any word' matching
    # "blue" is in "The sky is blue"
    wisdom = await kcp.synthesize_wisdom("Is it blue")
    assert "The sky is blue" in wisdom

def test_graph_structure():
    graph = SimpleKnowledgeGraph()
    graph.load_mock_data()

    a1 = graph.get_node("A1")
    assert a1.content == "Maximize efficiency and profit at all costs."

    conflicts = graph.get_related_ids("A1", "conflicts_with")
    assert "B1" in conflicts
