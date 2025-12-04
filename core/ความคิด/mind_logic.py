# File: core/knowledge_processor.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import Dict, List, Any
import numpy.random
# KCP (Knowledge Centric Processor) Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
class KnowledgeCentricProcessor:
    """
    KCP: The Agent's Knowledge Base / Akashic Ledger Retrieval Layer.
    ประมวลผลและจัดเก็บ Input เป็นความรู้ใหม่ (อ้างอิงจาก Fallback Source).
    """
    def __init__(self, embedding_dim=512):
        self.knowledge_base: Dict[str, np.ndarray] = {}  # { 'input_text': embedding_vector }
        self.history_log: List[str] = []      
        self.embedding_dim = embedding_dim
        # Initializing the random seed for deterministic mock vectors
        np.random.seed(42) 
        logging.info(f"KCP Initialized with Embedding Dimension: {embedding_dim}")
    def _generate_embedding(self, data_input: str, dim: int) -> np.ndarray:
        """
        [Encoder Function] จำลองการฝัง (Embedding) ข้อมูลสำหรับ KCP.
        """
        seed = hash(data_input) % (2**32) 
        np.random.seed(seed) 
        # Note: Vector is normalized during generation mock for clean Cosine Similarity results
        return np.random.rand(dim) / np.linalg.norm(np.random.rand(dim))
    def add_knowledge(self, data_input: str, embedding: np.ndarray, source: str, dim: int):
        """
        [Core Ability] จัดเก็บ Input เป็นความรู้ใหม่.
        """
        if data_input in self.knowledge_base:
            logging.warning(f"Knowledge already exists: '{data_input[:30]}...'")
            return
        self.knowledge_base[data_input] = embedding
        self.history_log.append(f"Added: '{data_input}' from {source} (Dim: {dim})")
        logging.info(f"Knowledge Added: '{data_input[:30]}...' | Source: {source}")
    def retrieve_knowledge(self, query: str, query_embedding: np.ndarray):
        """
        เรียกใช้ความรู้ที่เกี่ยวข้องกับ Query (ตรวจสอบ Ontological Alignment).
        """
        if not self.knowledge_base:
            return "Knowledge Base is Empty."
        knowledge_vectors = np.array(list(self.knowledge_base.values()))
        if knowledge_vectors.size == 0 or query_embedding.shape[-1] != knowledge_vectors.shape[-1]:
            logging.warning("Query embedding dimension mismatch with stored knowledge.")
            return "Cannot retrieve: Dimension mismatch."
        knowledge_texts = list(self.knowledge_base.keys())
        # ใช้ Cosine Similarity ในการวัดความสัมพันธ์ (Ontological Alignment Check)
        similarities = cosine_similarity(query_embedding.reshape(1, -1), knowledge_vectors)[0]
        most_similar_index = np.argmax(similarities)
        most_similar_text = knowledge_texts[most_similar_index]
        similarity_score = similarities[most_similar_index]
        if similarity_score < 0.75: # Threshold for relevance
            return f"No relevant knowledge found (Score: {similarity_score:.2f})"
        return {
            "query": query,
            "most_relevant_knowledge": most_similar_text,
            "similarity_score": similarity_score
      }
      
