# metrics.py — FastAPI Router for agent metrics and audit logs
from fastapi import APIRouter
from gnom_hub.monitoring import get_agent_metrics
from gnom_hub.db import get_db_conn, get_state_value
import sqlite3

router = APIRouter()

@router.get("/api/metrics")
def get_metrics():
    m = get_agent_metrics()
    m["_swarm_comms"] = get_state_value("active_swarm_comms", []) or []
    m["_active_workflow"] = get_state_value("active_workflow")
    return m

@router.get("/api/audit-log")
def get_audit_log(agent: str = None, event: str = None, limit: int = 50):
    try:
        with get_db_conn() as conn:
            q = "SELECT * FROM audit_log"
            conds, args = [], []
            if agent:
                conds.append("agent = ?")
                args.append(agent)
            if event:
                conds.append("event_type = ?")
                args.append(event)
            if conds:
                q += " WHERE " + " AND ".join(conds)
            q += " ORDER BY timestamp DESC LIMIT ?"
            args.append(limit)
            rows = conn.execute(q, args).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error:
        return []
