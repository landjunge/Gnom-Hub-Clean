"""Chat-Commands: clear-Varianten und Datenbereinigung."""
from .db import get_db, save_db
from .chat_commands import _post_chat

def handle_clear(q=""):
    q = q.strip().lower()
    if q == "all agents":
        sys_ags = ['soulag', 'generalag', 'securityag', 'watchdogag']
        save_db("agents", [a for a in get_db("agents") if a["name"].lower() in sys_ags])
        _post_chat("System", "Alle externen Agenten gelöscht. System-Infrastruktur bleibt intakt.")
        return {"status": "agents_cleared"}
    
    from .db import get_active_project
    p = get_active_project()
    
    if q == "@projekt":
        save_db("memory", [m for m in get_db("memory") if not (m.get("agent_id") == "war-room" and m.get("project", "default") == p)])
        import os, shutil
        from .routes_workspace import get_workspace_dir
        wd = get_workspace_dir()
        for f in os.listdir(wd):
            fp = os.path.join(wd, f)
            if os.path.isfile(fp): os.unlink(fp)
            elif os.path.isdir(fp): shutil.rmtree(fp)
        _post_chat("System", f"Projekt '{p}' komplett geleert.")
        return {"status": "project_cleared"}
        
    if q.startswith("chat"):
        parts = q.split()
        if len(parts) > 1:
            target_agent = parts[1].replace("@", "").lower()
            save_db("memory", [m for m in get_db("memory") if not (m.get("agent_id") == "war-room" and m.get("project", "default") == p and m.get("metadata", {}).get("sender", "").lower() == target_agent)])
            _post_chat("System", f"Chat-Historie von '{target_agent}' gelöscht.")
        else:
            save_db("memory", [m for m in get_db("memory") if not (m.get("agent_id") == "war-room" and m.get("project", "default") == p)])
            _post_chat("System", f"Kompletter Chat im Projekt '{p}' gelöscht.")
        return {"status": "cleared"}

    save_db("memory", [m for m in get_db("memory") if not (m.get("agent_id") == "war-room" and m.get("project", "default") == p)])
    return {"status": "cleared"}
