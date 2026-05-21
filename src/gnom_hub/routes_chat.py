from fastapi import APIRouter; from datetime import datetime; import uuid, re; from .db import get_db, save_db, get_active_project; from .brainstorm import dispatch; from .chat_commands import handle_idea, handle_clear, handle_status, handle_job, handle_free, handle_git, handle_publish; from pydantic import BaseModel
router = APIRouter()
class ChatMsg(BaseModel): content: str; sender: str = "user"
def _parse(t):
    m = re.match(r"@{1,2}(\w+)\s*(.*)", t, re.DOTALL); r, tag = m.group(2).strip() if m else None, m.group(1).lower() if m else None
    if not m: return t, None, None
    if tag in ("bs","clear","status","research","job","free","git","project"): return r or t, None, tag
    return r or t, tag, None
def _role(n, r):
    ags = get_db("agents"); a = next((x for x in ags if x["name"].lower() == n.lower()), None)
    if not a: return None
    [x.update({"role": "normal"}) for x in ags if x.get("role") == r and r != "normal"]; a["role"] = r; save_db("agents", ags); return a["name"]
def _handle_sys(q, m):
    from .chat_commands import _post_chat
    if m=="proj":
        from .db import set_active_project; set_active_project(q or "default")
        _post_chat("System", f"Project: {q or 'default'}")
    return {"status": "ok"}
CMDS = {"clear": handle_clear, "status": lambda q: handle_status(), "job": handle_job, "free": handle_free, "git": handle_git, "project": lambda q: _handle_sys(q,"proj")}
@router.post("/api/chat")
def post_chat(msg: ChatMsg):
    q, tgt, cmd = _parse(msg.content); s_name = msg.sender if msg.sender != "user" else tgt; from agents.securityAG import seal_content
    a = next((x for x in get_db("agents") if x.get("name","").lower() == (s_name or "").lower()), None)
    if a: msg.content = seal_content(a["name"], msg.content)
    save_db("memory", get_db("memory") + [{"id": str(uuid.uuid4()), "agent_id": "war-room", "project": get_active_project(), "content": msg.content, "metadata": {"type": cmd or "chat", "sender": msg.sender}, "timestamp": datetime.utcnow().isoformat()+"Z"}])
    if msg.sender != "user": return {"status": "saved"}
    if cmd in CMDS: return CMDS[cmd](q)
    if cmd == "research": return {"status": "dispatched", "asked": [n for n in [a["name"] for a in get_db("agents") if a.get("status")=="online" and a.get("role") != "general"] if dispatch(q, target=n)], "target": None, "mode": "research"}
    if not cmd and not tgt:
        dispatch(msg.content, target="GeneralAG")
        return {"status": "dispatched", "asked": ["GeneralAG"], "target": "GeneralAG", "mode": "chat"}
    return {"status": "dispatched", "asked": dispatch(q, target=tgt), "target": tgt, "mode": "brainstorm" if cmd=="bs" else "chat"}
@router.get("/api/chat")
def get_chat(limit: int = 50): 
    from .showbox_validator import sanitize_showboxes; rm = sorted([m for m in get_db("memory") if m.get("agent_id")=="war-room" and m.get("project", "default") == get_active_project()], key=lambda x: x.get("timestamp",""), reverse=True)[:limit]
    for m in rm:
        if "content" in m: m["content"] = sanitize_showboxes(m["content"])
    return rm