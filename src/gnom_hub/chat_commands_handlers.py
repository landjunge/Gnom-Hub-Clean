import uuid, re, subprocess
from datetime import datetime
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.infrastructure.database.agent_repo import SQLiteAgentRepository
from gnom_hub.infrastructure.database.chat_repo import SQLiteChatRepository
from gnom_hub.domain.chat.entities import ChatMessage

def _post_chat(s, c):
    proj = SQLiteStateRepository().get_active_project()
    m = ChatMessage(id=str(uuid.uuid4()), project=proj, sender=s, agent_id="war-room", msg_type="role_response", content=c, timestamp=datetime.utcnow())
    SQLiteChatRepository().add_message(m)

def handle_clear(q=""):
    from .chat_clear import handle_clear as _hc
    return _hc(q)

def handle_status():
    return {"agents": [{"name": a.name, "role": a.role, "st": a.status} for a in SQLiteAgentRepository().get_all()]}

def handle_free(q):
    t = q.replace("@","").strip().lower()
    SQLiteAgentRepository().clear_jobs(t or None)
    _post_chat("System", f"Jobs cleared: {t or 'ALL'}")
    return {"status": "ok"}

def handle_job(task):
    from .role_tools import distribute_job; from .application.chat.brainstorm import dispatch
    agent_repo, state_repo = SQLiteAgentRepository(), SQLiteStateRepository()
    ags = agent_repo.get_all()
    gen = next((a for a in ags if a.role == "general" or a.name.lower() == "generalag"), None)
    if not gen: return {"error": "Kein General"}
    jobs = state_repo.get_value("jobs", []) + [{"id": str(uuid.uuid4()), "task": task, "general": gen.name, "status": "open", "ts": datetime.utcnow().isoformat()+"Z"}]
    state_repo.set_value("jobs", jobs); res = distribute_job(task); _post_chat(gen.name, res)
    for a in ags:
        aj = next((m.group(2).strip() for m in re.finditer(r'@(\w+)[\s→>:\-]+(.+)', res) if m.group(1).lower() == a.name.lower()), "")
        agent_repo.update_active_job(a.name, aj)
        if aj: dispatch(aj, target=a.name)
    return {"status": "job_created"}

def handle_git(q, rb=False):
    p = q.split(" ", 1); cmd = f"reset --hard {p[1]}" if rb else (p[1] if len(p) > 1 else "")
    from pathlib import Path
    if not (Path(".") / ".git").exists(): subprocess.run(["git", "init"], capture_output=True)
    try: r = subprocess.run(["git"] + cmd.split(), capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception as e: r = f"Error: {e}"
    _post_chat("System", f"Git: {r[:300]}"); return {"status": "ok"}
