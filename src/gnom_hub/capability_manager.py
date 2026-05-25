# capability_manager.py — capability manager
import sqlite3
from datetime import datetime, timezone, timedelta
from gnom_hub.db import get_db_conn

def request_capability(agent_name: str, cap_type: str, resource: str, granted_by: str, ttl_min: int = 5) -> bool:
    exp = (datetime.now(timezone.utc) + timedelta(minutes=ttl_min)).isoformat().replace("+00:00", "Z")
    try:
        with get_db_conn() as conn:
            with conn:
                conn.execute("""
                    INSERT OR REPLACE INTO capabilities (id, agent_name, capability_type, resource, granted_by, expires_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (f"{agent_name}_{cap_type}_{resource}", agent_name, cap_type, resource, granted_by, exp))
                return True
    except Exception: return False

def check_capability(agent_name: str, cap_type: str, resource: str) -> bool:
    cleanup_expired()
    try:
        with get_db_conn() as conn:
            row = conn.execute("""
                SELECT 1 FROM capabilities
                WHERE agent_name = ? AND capability_type = ? AND resource = ? AND is_active = 1
            """, (agent_name, cap_type, resource)).fetchone()
            return row is not None
    except Exception: return False

def cleanup_expired():
    now_str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        with get_db_conn() as conn:
            with conn:
                conn.execute("UPDATE capabilities SET is_active = 0 WHERE expires_at <= ?", (now_str,))
    except Exception: pass
