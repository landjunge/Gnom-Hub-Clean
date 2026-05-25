# embeddings.py — Local embeddings / semantic retrieval helper
from gnom_hub.semantic_memory_retriever import SemanticMemoryRetriever
import gnom_hub.smr_retrieve as sr

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

class SoulEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", db_path: str = "gnomhub.db"):
        self.db_path = db_path
        self.smr = SemanticMemoryRetriever()
        self.helper = None
        if HAS_LIBS:
            from gnom_hub.emb_faiss import FaissEmbeddingHelper
            self.helper = FaissEmbeddingHelper(model_name, db_path)

    def add_fact(self, fact_id: str, key: str, value: str):
        if self.helper: self.helper.add_fact(fact_id, key, value)

    def search_sync(self, query: str, top_k: int = 8) -> list:
        if self.helper:
            res = self.helper.search(query, top_k)
            if res: return res
        return sr.retrieve_similar_sync(query, top_k)

    async def search(self, query: str, top_k: int = 8) -> list:
        return self.search_sync(query, top_k)
