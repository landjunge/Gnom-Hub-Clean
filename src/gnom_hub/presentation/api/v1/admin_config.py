from fastapi import APIRouter, Request
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.infrastructure.database.agent_role import set_agent_role, update_agent_role_memory

router = APIRouter(prefix="/api/admin")

ROLES = {
    "de": {"general": "SYSTEM-ROLLE: GENERAL. Task-Verteilung, Koordination. Analysiere @job und verteile Aufgaben via @Name -> Aufgabe. Keine Erklärungen."},
    "en": {"general": "SYSTEM ROLE: GENERAL. Task distribution and coordination. Analyze @job and distribute tasks via @Name -> Task. No explanations."}
}

@router.put("/agents/{agent_id}/role")
def set_role(agent_id: str, role: str):
    state_repo = SQLiteStateRepository()
    lang = state_repo.get_language()
    roles_dict = ROLES[lang]
    if role not in ("general", "normal"): return {"error": "Invalid role"}
    agent = set_agent_role(agent_id, role)
    if not agent: return {"error": "Agent not found"}
    role_content = roles_dict[role] if role in roles_dict else None
    update_agent_role_memory(agent["id"], role_content)
    from gnom_hub.role_prompt import implant
    file_path = implant(agent["name"], role_content) if role_content else None
    return {"agent": agent["name"], "role": role, "file": file_path}

@router.get("/language")
def get_sys_language():
    return {"language": SQLiteStateRepository().get_language()}

@router.post("/language")
async def set_sys_language(req: Request):
    j = await req.json()
    SQLiteStateRepository().set_language(j.get("language", "en"))
    return {"status": "ok"}
