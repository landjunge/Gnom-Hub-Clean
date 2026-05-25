import re
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.chat_commands import _post_chat

def _parse(t):
    t_clean = t.strip()
    m_gen = re.match(r"@generalag\s+@(\w+)\s*(.*)", t_clean, re.IGNORECASE | re.DOTALL)
    if m_gen:
        tag = m_gen.group(1).lower()
        if tag in ("bs","clear","status","research","job","free","git","project"):
            return m_gen.group(2).strip(), None, tag
    m = re.match(r"@{1,2}(\w+)\s*(.*)", t_clean, re.DOTALL)
    r, tag = (m.group(2).strip() if m else None), (m.group(1).lower() if m else None)
    if not m: return t_clean, None, None
    if tag in ("bs","clear","status","research","job","free","git","project"):
        return r or t_clean, None, tag
    return r or t_clean, tag, None

def _handle_sys(q, m):
    if m == "proj":
        SQLiteStateRepository().set_active_project(q or "default")
        _post_chat("System", f"Project: {q or 'default'}")
    return {"status": "ok"}
