import requests, os, json as _json; PORT = os.environ.get("GNOM_HUB_PORT", "3002")
def api(m, p, **k):
    try: return _json.dumps(requests.request(m, f"http://127.0.0.1:{PORT}/api{p}", **k).json())
    except: return "Err"
TOOLS = {}
def tool(fn): TOOLS[fn.__name__] = fn; return fn
@tool
def save_to_memory(a, c): return api("POST", "/memory", json={"agent_id": a, "content": c})
@tool
def get_memory(a): return api("GET", f"/agents/{a}/memory")
@tool
def list_all_agents(): return api("GET", "/agents")
@tool
def get_agent(a): return api("GET", f"/agents/{a}")
@tool
def war_room_chat(m, s="mcp"): return api("POST", "/chat", json={"content": m, "sender": s})
@tool
def war_room_read(limit=20): return api("GET", f"/chat?limit={limit}")
@tool
def get_system_stats(): return api("GET", "/stats")
@tool
def smart_crawl(cmd):
    from .router import ask_router
    from .smart_crawl import smart_request
    try:
        resp = ask_router(cmd, "Extrahiere nur die URL aus dem Befehl. Gib NUR die URL zurück.", agent_name="GeneralAG")
        url = resp.strip()
        if not url.startswith("http"): return "❌ Keine valide URL gefunden."
        return smart_request(url)
    except Exception as e: return f"❌ Crawl fehlgeschlagen: {e}"
@tool
def data_crawl(cmd):
    from .router import ask_router
    from .crawler_engine import rotate_user_agent, _load, _save, _dom
    import requests, time
    try:
        resp = ask_router(cmd, "Extrahiere nur die reine URL. Kein Zusatztext.", agent_name="GeneralAG")
        url = resp.strip()
        if not url.startswith("http"): return "❌ Keine valide URL gefunden."
        headers = {"User-Agent": rotate_user_agent(), "Accept": "application/json, text/html, */*"}
        r = requests.get(url, timeout=20, headers=headers)
        db, dom = _load(), _dom(url)
        db.setdefault(dom, {"blocks": 0, "last": 0})["last"] = time.time(); _save(db)
        html = r.text[:12000]
        return ask_router(f"URL: {url}\nHTML: {html}", "Extrahiere alle strukturierten Daten (Tabellen, Listen, Preise, JSON). Gib sauberes Ergebnis.", agent_name="GeneralAG")
    except Exception as e: return f"❌ Data-Crawl Fehler: {str(e)}"
@tool
def web_crawl(cmd):
    from .router import ask_router
    from .crawler_engine import rotate_user_agent, _load, _save, _dom
    import requests, time, re
    try:
        resp = ask_router(cmd, "Extrahiere nur die reine URL. Kein Zusatztext.", agent_name="GeneralAG")
        url = resp.strip()
        if not url.startswith("http"): return "❌ Keine valide URL gefunden."
        r = requests.get(url, timeout=15, headers={"User-Agent": rotate_user_agent()})
        db, dom = _load(), _dom(url)
        db.setdefault(dom, {"blocks": 0, "last": 0})["last"] = time.time(); _save(db)
        text = re.sub(r'<[^>]+>', ' ', r.text)
        return re.sub(r'\s+', ' ', text).strip()[:8000]
    except Exception as e: return f"❌ Web-Crawl Fehler: {str(e)}"
@tool
def get_agent_soul(name): from .soul_initializer import get_soul; return _json.dumps(get_soul(name))
@tool
def run_tool(name, **kwargs): return TOOLS[name](**kwargs) if name in TOOLS else f"Tool '{name}' nicht gefunden."
