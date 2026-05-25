# soul_retrieval.py — Semantic Retrieval via local embeddings / fallbacks
from .db import get_db_conn
from .embeddings import SoulEmbedder

def retrieve_relevant_facts(query: str, top_k: int = 5) -> list:
    try:
        facts = SoulEmbedder().search_sync(query, top_k)
        if facts: return facts
    except Exception: pass
    return _fetch_recent(top_k)

def _fetch_recent(limit: int) -> list:
    try:
        with get_db_conn() as conn:
            rows = conn.execute("SELECT key, value FROM soul_memory ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
            return [f"{r['key']}: {r['value']}" for r in rows]
    except Exception: return []
