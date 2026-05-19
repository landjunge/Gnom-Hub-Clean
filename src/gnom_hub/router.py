import requests, time; from .router_config import DS_KEY, OR_KEY, AGENT_MODELS, DEFAULT_MODELS, get_key_for; from .router_tokens import track_tokens
def _ext(d, a, m):
    c = d.get("choices", [])
    if c and c[0].get("message", {}).get("content"):
        if d.get("usage"): track_tokens(a or "?", m, d["usage"])
        print(f"[ROUTER] Erfolg: {a} auf {m}"); return c[0]["message"]["content"]
    return None
def ask_router(p, sys="Du bist ein Assistent.", agent_name=None):
    n, msgs = (agent_name or "").lower(), [{"role": "system", "content": sys}, {"role": "user", "content": p}]
    if DS_KEY:
        try:
            print(f"\n[ROUTER] {agent_name or '?'} → DeepSeek...")
            r = requests.post("https://api.deepseek.com/chat/completions", headers={"Authorization": f"Bearer {DS_KEY}", "Content-Type": "application/json"}, json={"model": "deepseek-chat", "messages": msgs}, timeout=120)
            if r.status_code == 200:
                ans = _ext(r.json(), agent_name, "deepseek-chat")
                if ans: return ans
            print(f"[ROUTER] DeepSeek: {r.status_code}. Fallback...")
        except Exception as e: print(f"[ROUTER] DeepSeek Fehler: {e}. Fallback...")
    for m in AGENT_MODELS.get(n, DEFAULT_MODELS):
        if not OR_KEY: continue
        try:
            print(f"[ROUTER] {agent_name or '?'} → {m}...")
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"}, json={"model": m, "messages": msgs}, timeout=120)
            if r.status_code == 200:
                ans = _ext(r.json(), agent_name, m)
                if ans: return ans
                print(f"[ROUTER] {m}: leere Antwort. Nächstes...")
            elif r.status_code == 429: print(f"[ROUTER] {m}: Rate-Limit. Warte 2s..."); time.sleep(2)
            else: print(f"[ROUTER] {m} gescheitert ({r.status_code}).")
        except Exception as e: print(f"[ROUTER] Absturz auf {m}: {e}")
    return "[ROUTER-FEHLER] Alle Gleise offline."
