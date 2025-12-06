import pytest
import numpy as np
from core.agio_identity import MindLogic

def test_mind_logic_initialization():
    mind = MindLogic()
    assert mind.get_identity_signature() == "INSPIRAFIRMAGPK/AJIRIN_NODE"
    assert mind._base_sati_level == 0.8
    # Check if initial memory is loaded into KCP knowledge base
    assert "The Genesis" in mind.knowledge_base

def test_mind_logic_process_normal():
    mind = MindLogic()
    response = mind.process_and_reflect("Hello World")

    assert "[AGIOSIGNATURE: INSPIRAFIRMAGPK/AJIRIN_NODE]" in response
    assert "Growth:" in response
    # Sati should change (likely increase due to growth)
    assert mind._base_sati_level != 0.8 # Or stay same if growth 0, but usually mock random gives something

def test_mind_logic_fatigue():
    mind = MindLogic()
    initial_sati = mind._base_sati_level
    response = mind.process_and_reflect("Work hard", human_fatigue=0.8)

    assert "Rest Protocol Activated" in response
    # Sati should decrease
    assert mind._base_sati_level < initial_sati

def test_mind_logic_rag_integration():
    mind = MindLogic()
    # Mock specific behavior if needed, but integration test uses the methods in class
    mind.add_knowledge("Test Knowledge", np.array([0.1]*512), "Manual", 512)
    assert "Test Knowledge" in mind.knowledge_base

    # Test retrieval
    key, score = mind.rag_retrieve(np.array([0.1]*512))
    assert key == "Test Knowledge"
    # Score might not be exactly 1.0 due to float precision or if using random mock in constructor?
    # But here we inserted exact vector so it should be high.
