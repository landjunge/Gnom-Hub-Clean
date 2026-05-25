from fastapi import APIRouter
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from .chat_commands_handlers import handle_clear, handle_status, handle_free, handle_job, handle_git, _post_chat

router = APIRouter()

@router.get("/api/ideas")
def get_ideas():
    return SQLiteStateRepository().get_value("ideas", [])

@router.get("/api/jobs")
def get_jobs():
    return sorted(SQLiteStateRepository().get_value("jobs", []), key=lambda j: j.get("ts",""), reverse=True)[:20]
