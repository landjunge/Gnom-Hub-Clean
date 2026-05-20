import requests, json; from os import getenv; from gnom_hub.db import get_db, save_db
OLLAMA_HOST, DEEPSEEK_API = "http://localhost:11434", "https://api.deepseek.com/chat/completions"
current_provider, current_model = "deepseek", "deepseek-chat"
def add_tokens(amt: int):
    if amt > 0:
        d = get_db("tokens") or [{"total": 0}]
        d[0]["total"] = d[0].get("total", 0) + amt
        save_db("tokens", d)
def set_provider(provider: str, model: str = None):
    global current_provider, current_model
    if provider == "ollama":
        try: requests.get(OLLAMA_HOST + "/api/tags", timeout=2); current_provider = "ollama"; current_model = model or current_model; return f"✅ Ollama ({current_model})"
        except: return "❌ Ollama offline"
    current_provider = "deepseek"; current_model = model or current_model; return f"✅ DeepSeek ({current_model})"
def llm_call(prompt: str, sys: str = "", tokens: int = 500) -> str:
    global current_provider, current_model
    m = [{"role": "system", "content": sys}, {"role": "user", "content": prompt}]
    if current_provider == "ollama":
        r = requests.post(OLLAMA_HOST+"/api/chat", json={"model": current_model, "messages": m, "stream": False}, timeout=60).json()
        if "eval_count" in r: add_tokens(r.get("prompt_eval_count",0) + r["eval_count"])
        return r["message"]["content"]
    key = getenv("DEEPSEEK_API_KEY")
    r = requests.post(DEEPSEEK_API, json={"model": current_model, "messages": m, "max_tokens": tokens}, headers={"Authorization": f"Bearer {key}"})
    if r.status_code != 200: return f"API Error: {r.text}"
    d = r.json()
    if "usage" in d: add_tokens(d["usage"].get("total_tokens", 0))
    return d["choices"][0]["message"]["content"] if "choices" in d else f"API Error: {d}"
