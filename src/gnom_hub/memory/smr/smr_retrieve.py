# smr_retrieve.py
from gnom_hub.db.legacy_db import get_db_conn
from gnom_hub.memory.smr.smr_math import cosine_similarity

def retrieve_similar_sync(query: str, agent_name: str = None, top_k: int = 8, raw: bool = False) -> list:
    try:
        with get_db_conn() as conn:
            if agent_name:
                rows = conn.execute(
                    "SELECT key, value, priority FROM soul_memory WHERE agent IS NULL OR LOWER(agent) IN ('system', 'all', 'soulag', ?)",
                    (agent_name.lower(),)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT key, value, priority FROM soul_memory WHERE agent IS NULL OR LOWER(agent) IN ('system', 'all', 'soulag')"
                ).fetchall()
        if not rows: return []
        scored = []
        for r in rows:
            sc = cosine_similarity(query, r["value"])
            if sc < 0.60:
                continue
            if not raw:
                p = (r["priority"] or "medium").lower()
                weight = 1.3 if p == "high" else (0.7 if p == "low" else 1.0)
                sc = sc * weight
            scored.append((sc, f"{r['key']}: {r['value']}"))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [fact for sc, fact in scored[:top_k] if sc > 0.0]
    except Exception: return []

async def retrieve_similar(query: str, agent_name: str = None, top_k: int = 8, raw: bool = False) -> list:
    return retrieve_similar_sync(query, agent_name=agent_name, top_k=top_k, raw=raw)

async def retrieve_with_fallback(query: str, agent_name: str = None, top_k: int = 8) -> list:
    similar = await retrieve_similar(query, agent_name=agent_name, top_k=top_k)
    if similar: return similar
    try:
        with get_db_conn() as conn:
            if agent_name:
                rows = conn.execute(
                    "SELECT key, value FROM soul_memory WHERE agent IS NULL OR LOWER(agent) IN ('system', 'all', 'soulag', ?) ORDER BY timestamp DESC LIMIT ?",
                    (agent_name.lower(), top_k)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT key, value FROM soul_memory WHERE agent IS NULL OR LOWER(agent) IN ('system', 'all', 'soulag') ORDER BY timestamp DESC LIMIT ?",
                    (top_k,)
                ).fetchall()
            return [f"{r['key']}: {r['value']}" for r in rows]
    except Exception: return []
