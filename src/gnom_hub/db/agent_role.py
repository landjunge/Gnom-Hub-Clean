import json, uuid
from datetime import datetime, timezone
from typing import Optional
from .connection import get_db_conn

def set_agent_role(agent_ref: str, role: str) -> Optional[dict]:
    with get_db_conn() as c, c:
        row = c.execute("SELECT name FROM agents WHERE id = ? OR name = ?", (agent_ref, agent_ref)).fetchone()
        name = row["name"] if row else agent_ref
        from gnom_hub.db.legacy_db import validate_agent_limit_db
        validate_agent_limit_db(c, role, name)
        if role == "general":
            c.execute("UPDATE agents SET role = 'normal' WHERE role = 'general'")
        c.execute("UPDATE agents SET role = ? WHERE id = ? OR name = ?", (role, agent_ref, agent_ref))
        row = c.execute("SELECT * FROM agents WHERE id = ? OR name = ?", (agent_ref, agent_ref)).fetchone()
        return dict(row) if row else None

def update_agent_role_memory(agent_id: str, role_content: str = None) -> None:
    with get_db_conn() as c, c:
        c.execute("DELETE FROM chat WHERE agent_id = ? AND msg_type = 'role'", (agent_id,))
        if role_content:
            c.execute("""
                INSERT INTO chat (id, project, sender, agent_id, msg_type, content, timestamp, metadata)
                VALUES (?, 'default', 'System', ?, 'role', ?, ?, ?)
            """, (str(uuid.uuid4()), agent_id, role_content, datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), json.dumps({"type": "role", "sender": "System"})))
