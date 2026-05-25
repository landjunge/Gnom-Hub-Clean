import json; from uuid import UUID; from datetime import datetime; from typing import List, Optional
from gnom_hub.domain.agent.entities import Agent
from gnom_hub.domain.agent.repository import AgentRepository
from .connection import get_db_connection, Await, parse_dt

def _to_ag(r) -> Optional[Agent]:
    if not r: return None
    return Agent(id=UUID(r["id"]), name=r["name"], status=r["status"], pid=r["pid"], model=r["model"], last_seen=parse_dt(r["last_seen"]),
                 port=r["port"], description=r["description"], capabilities=json.loads(r["capabilities"] or "[]"), role=r["role"], active_job=r["active_job"])

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
            ls = a.last_seen.isoformat() if a.last_seen else None
            conn.execute("INSERT OR REPLACE INTO agents (id, name, status, pid, model, last_seen, port, description, capabilities, role, active_job, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (str(a.id), a.name, a.status, a.pid, a.model, ls, a.port, a.description, json.dumps(a.capabilities or []), a.role, a.active_job))
            conn.commit()
        return Await(a)
    def delete(self, a_id) -> Await:
        with get_db_connection() as conn:
            cur = conn.execute("DELETE FROM agents WHERE id = ? OR name = ?", (str(a_id), str(a_id)))
            conn.commit()
            return Await(cur.rowcount > 0)
    def delete_by_id(self, a_id) -> None: self.delete(a_id)
    def delete_offline(self) -> None:
        with get_db_connection() as conn: conn.execute("DELETE FROM agents WHERE status = 'offline'"); conn.commit()
    def update_status(self, name: str, status: str) -> None:
        with get_db_connection() as conn: conn.execute("UPDATE agents SET status = ?, last_seen = ? WHERE name = ?", (status, datetime.now().isoformat(), name)); conn.commit()
