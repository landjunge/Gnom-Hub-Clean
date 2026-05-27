from fastapi import APIRouter
from pydantic import BaseModel
from gnom_hub.db.state_repo import SQLiteStateRepository

router = APIRouter(prefix="/api/admin")

class ToolDef(BaseModel):
    name: str
    description: str = ""
    method: str = "GET"
    path: str = ""

@router.get("/tools")
def list_tools():
    return SQLiteStateRepository().get_value("tools", [])

@router.post("/tools")
def register_tool(t: ToolDef):
    repo = SQLiteStateRepository()
    tools = [x for x in repo.get_value("tools", []) if x["name"] != t.name] + [t.dict()]
    repo.set_value("tools", tools)
    return {"registered": t.name}

@router.delete("/tools/{name}")
def remove_tool(name: str):
    repo = SQLiteStateRepository()
    tools = [t for t in repo.get_value("tools", []) if t["name"] != name]
    repo.set_value("tools", tools)
    return {"removed": name}
