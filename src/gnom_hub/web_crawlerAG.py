"""web_crawlerAG: Allgemeiner Web-Surfer — holt Rohdaten."""
import requests, re, random
from .smart_crawl import rotate_user_agent, _load, _save, _dom
from .router import ask_router
from .gitAG import auto_commit

def web_crawl(command: str) -> str:
    """Holt Webseiten-Inhalt als Rohtext."""
    try:
        resp = ask_router(command, "Extrahiere nur die reine URL. Kein Zusatztext.", agent_name="web_crawlerAG")
        url = resp.strip()
        if not url.startswith("http"):
            return "❌ Keine valide URL gefunden."
        r = requests.get(url, timeout=15, headers={"User-Agent": rotate_user_agent()})
        db, dom = _load(), _dom(url)
        db.setdefault(dom, {"blocks": 0, "last": 0})
        import time; db[dom]["last"] = time.time()
        _save(db)
        text = re.sub(r'<[^>]+>', ' ', r.text)
        auto_commit(".")
        return re.sub(r'\s+', ' ', text).strip()[:8000]
    except Exception as e:
        return f"❌ Web-Crawl Fehler: {str(e)}"
