import requests, time; from .router_config import DS_KEY, OR_KEY, AGENT_MODELS, DEFAULT_MODELS; from .router_tokens import track_tokens; from .db import get_db
def _ext(d, a, m):
    c = d.get("choices", [])
    if c and c[0].get("message", {}).get("content"):
        if d.get("usage"): track_tokens(a or "?", m, d["usage"])
        return c[0]["message"]["content"]
    return None
def _call(pvd, mdl, key, msgs, n):
    url = "https://api.deepseek.com/chat/completions" if pvd == "deepseek" else "https://openrouter.ai/api/v1/chat/completions"
    r = requests.post(url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json={"model": mdl, "messages": msgs}, timeout=120)
    if r.status_code == 200: return _ext(r.json(), n, mdl)
    if r.status_code == 429: time.sleep(2)
    return None
def ask_router(p, sys="Du bist ein Assistent.", agent_name=None):
    n, msgs = (agent_name or "").lower(), [{"role": "system", "content": sys}, {"role": "user", "content": p}]
    kdb, adb = get_db("llm_keys") or {}, get_db("llm_agents") or {}
    cfg = adb.get(n)
    if cfg and cfg.get("provider") and cfg.get("model") and cfg.get("key_id"):
        key = kdb.get(cfg["key_id"], {}).get("key")
        if key:
            try:
                ans = _call(cfg["provider"], cfg["model"], key, msgs, agent_name)
                if ans: return ans
            except: pass
    if DS_KEY:
        try:
            ans = _call("deepseek", "deepseek-chat", DS_KEY, msgs, agent_name)
            if ans: return ans
        except: pass
    for m in AGENT_MODELS.get(n, DEFAULT_MODELS):
        if not OR_KEY: continue
        try:
            ans = _call("openrouter", m, OR_KEY, msgs, agent_name)
            if ans: return ans
        except: pass
    return "[ROUTER-FEHLER] Alle Gleise offline."
