import subprocess
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.infrastructure.database.agent_repo import SQLiteAgentRepository
from .chat_commands_handlers import handle_clear, handle_status, handle_job, _post_chat

router = APIRouter()

@router.get("/help")
def get_help():
    return FileResponse(str(Path(__file__).parent.parent.parent / "frontend" / "help.html"))

@router.get("/api/ideas")
def get_ideas(): return SQLiteStateRepository().get_value("ideas", [])

@router.get("/api/jobs")
def get_jobs():
    return sorted(SQLiteStateRepository().get_value("jobs", []), key=lambda j: j.get("ts",""), reverse=True)[:20]

def handle_free(q):
    t = q.replace("@","").strip().lower()
    SQLiteAgentRepository().clear_jobs(t or None)
    _post_chat("System", f"Jobs cleared: {t or 'ALL'}")
    return {"status": "ok"}

def handle_git(q, rb=False):
    p = q.split(" ", 1); cmd = f"reset --hard {p[1]}" if rb else (p[1] if len(p) > 1 else "")
    from pathlib import Path
    if not (Path(".") / ".git").exists(): subprocess.run(["git", "init"], capture_output=True)
    try: r = subprocess.run(["git"] + cmd.split(), capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception as e: r = f"Error: {e}"
    _post_chat("System", f"Git: {r[:300]}"); return {"status": "ok"}
