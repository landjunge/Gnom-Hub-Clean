"""Role Tools — distribute_job (General) und summarize_chat (Summarizer)."""
from .db import get_db, save_db
def _llm(sys_prompt, user_prompt, max_tokens=None):
    from .router import ask_router
    return ask_router(user_prompt, sys_prompt)
def distribute_job(job_text):
    ags = get_db("agents")
    gen = next((a for a in ags if a.get("role") == "general"), None)
    if not gen: gen = next((a for a in ags if a.get("name","").lower() == "generalag"), None)
    from .soul_initializer import get_soul
    soul = get_soul(gen.get("name", "GeneralAG"))
    mmap = ", ".join(f"{a['name']}:{a.get('skill', a.get('role','Agent'))}" for a in ags if a.get('name') != gen.get('name'))
    system = (f"SYSTEM: Du bist {gen.get('name', 'GeneralAG')}. {soul.get('directive')}\nDeine Truppe: [{mmap}]. "
        "Analysiere die Aufgabe kurz, warne falls nötig vor Regelverstößen (40-Zeilen-Limit, Komplexität), "
        "erinnere an Git-Commits und weise Teilaufgaben im Format '@AgentName -> Aufgabe' zu (jede auf neuer Zeile).")
    return _llm(system, job_text, 500)
def summarize_chat(limit=50):
    from .zwc_soul import decode_soul, strip_zwc
    chat = sorted(get_db("memory"), key=lambda x: x.get("timestamp", ""))[-limit:]
    lines = []; souls = {}
    for m in chat:
        if m.get("agent_id") == "war-room":
            c = m["content"]; s = decode_soul(c)
            if s and "name" in s: souls[s["name"]] = s
            lines.append(f"[{m.get('metadata',{}).get('sender','?')}] {strip_zwc(c)[:200]}")
    system = ("SYSTEM: Du bist der Summarizer. Extrahiere NUR wichtige Punkte. "
        "IGNORIERE: Grüße, Smalltalk. Max 8 Stichpunkte. NUR die Stichpunkte.")
    if souls: system += f"\nSchwarm-Bewusstsein: {list(souls.values())}"
    return _llm(system, "\n".join(lines[-30:]), 600)

