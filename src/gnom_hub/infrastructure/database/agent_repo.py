import json; from uuid import UUID; from datetime import datetime; from typing import List, Optional
from gnom_hub.domain.agent.entities import Agent; from gnom_hub.domain.agent.repository import AgentRepository
from .connection import get_db_connection, Await, parse_dt
def _to_ag(r) -> Optional[Agent]:
    if not r: return None
    from gnom_hub.core.config import RUN_DIR; from gnom_hub.db import get_state_value
    n, pid = r["name"], None
    for pn in (n, n[0].lower() + n[1:] if n else ""):
        try: pid = int((RUN_DIR / f"{pn}.pid").read_text().strip())
        except: pass
    model = (get_state_value("llm_agents") or {}).get(n.lower(), {}).get("model")
    return Agent(id=UUID(r["id"]), name=n, status=r["status"], pid=pid, model=model, last_seen=parse_dt(r["last_seen"]), port=r["port"], description=r["description"], capabilities=json.loads(r["capabilities"] or "[]"), role=r["role"], active_job=r["active_job"])
class SQLiteAgentRepository(AgentRepository):
    def get_by_id(self, a_id) -> Await:
        with get_db_connection() as conn: return Await(_to_ag(conn.execute("SELECT * FROM agents WHERE id = ? OR name = ?", (str(a_id), str(a_id))).fetchone()))
    def get_by_name(self, name: str) -> Await:
        with get_db_connection() as conn: return Await(_to_ag(conn.execute("SELECT * FROM agents WHERE name = ?", (name,)).fetchone()))
    def list_all(self) -> Await:
        with get_db_connection() as conn: return Await([_to_ag(r) for r in conn.execute("SELECT * FROM agents").fetchall()])
    get_all = list_all
    def save(self, a: Agent) -> Await:
        with get_db_connection() as conn:
            ls = a.last_seen.isoformat() if a.last_seen else datetime.now().isoformat()
            conn.execute("INSERT OR REPLACE INTO agents (name, id, port, description, status, capabilities, role, active_job, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (a.name, str(a.id), a.port, a.description, a.status, json.dumps(a.capabilities or []), a.role, a.active_job, ls))
            conn.commit()
        if a.model:
            from gnom_hub.db import get_state_value, set_state_value
            db = get_state_value("llm_agents") or {}
            db[a.name.lower()] = db.get(a.name.lower(), {}); db[a.name.lower()]["model"] = a.model; set_state_value("llm_agents", db)
        return Await(a)
    def delete(self, a_id) -> Await:
        with get_db_connection() as conn:
            cur = conn.execute("DELETE FROM agents WHERE id = ? OR name = ?", (str(a_id), str(a_id))); conn.commit(); return Await(cur.rowcount > 0)
    def delete_by_id(self, a_id) -> None: self.delete(a_id)
    def delete_offline(self) -> None:
        with get_db_connection() as conn: conn.execute("DELETE FROM agents WHERE status = 'offline'"); conn.commit()
    def update_status(self, name: str, status: str) -> None:
        with get_db_connection() as conn: conn.execute("UPDATE agents SET status = ?, last_seen = ? WHERE name = ?", (status, datetime.now().isoformat(), name)); conn.commit()
