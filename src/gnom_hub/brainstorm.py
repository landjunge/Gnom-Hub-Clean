import threading; from .db import get_db; from .brainstorm_helpers import ask_llm, get_ctx
def _run_phase(ags, q, ctx, bs=False):
    ts = []
    for a in ags:
        t = threading.Thread(target=ask_llm, args=(a, q, ctx, bs), daemon=True); t.start(); ts.append(t)
    for t in ts: t.join(timeout=200)
def dispatch(q, target=None):
    ao = [a for a in get_db("agents") if a.get("status") == "online"]
    if target:
        s = [a for a in ao if a["name"].lower() == target.lower()]
        for a in s: threading.Thread(target=ask_llm, args=(a, q, get_ctx(), False), daemon=True).start()
        return [a["name"] for a in s]
    w = [a for a in ao if a["name"].lower() not in ("soulag", "generalag", "securityag", "watchdogag")]
    g = [a for a in ao if a["name"] == "GeneralAG"]
    print(f"[BS] Phase 1: Worker ({[a['name'] for a in w]})"); _run_phase(w, q, get_ctx(), True)
    if g: print(f"[BS] Phase 2: General"); _run_phase(g, q, get_ctx(), True)
    return [a["name"] for a in w + g]
