import requests, time, json
from .router_tokens import track_tokens
from .router_keys import get_keys

def _ext(d, a, m):
    c = d.get("choices", [])
    if c and c[0].get("message", {}).get("content"):
        if d.get("usage"): track_tokens(a or "?", m, d["usage"])
        return c[0]["message"]["content"]

def _call(pvd, mdl, key, msgs, n):
    h = {"Content-Type": "application/json"}
    if pvd == "anthropic":
        h.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
        sys = next((m["content"] for m in msgs if m["role"] == "system"), "")
        pyld = {"model": mdl, "max_tokens": 1024, "messages": [m for m in msgs if m["role"] != "system"]}
        if sys: pyld["system"] = sys
    else:
        urls = {"openai": "https://api.openai.com/v1/chat/completions", "mistral": "https://api.mistral.ai/v1/chat/completions", "gemini": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "deepseek": "https://api.deepseek.com/chat/completions", "openrouter": "https://openrouter.ai/api/v1/chat/completions", "lokal": "http://127.0.0.1:11434/api/chat"}
        url = urls.get(pvd, urls["openrouter"])
        if pvd != "lokal": h["Authorization"] = f"Bearer {key}"
        pyld = {"model": mdl, "messages": msgs}
        if pvd == "lokal": pyld["stream"] = False

    r = requests.post(url, headers=h, json=pyld, timeout=120)
    if r.status_code == 200:
        if pvd == "anthropic": return r.json().get("content", [{}])[0].get("text")
        if pvd != "lokal": return _ext(r.json(), n, mdl)
        return "".join(json.loads(l).get("message", {}).get("content", "") for l in r.text.strip().split("\n") if l).strip() or None
    if r.status_code == 429: time.sleep(2)

def _try_keys(pvd, mdl, kdb, msgs, an):
    for k in get_keys(pvd, kdb):
        try:
            ans = _call(pvd, mdl, k, msgs, an)
            if ans: return ans
        except Exception: pass
