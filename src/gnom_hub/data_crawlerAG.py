"""data_crawlerAG: Strukturierter Daten-Crawler (Tabellen, Listen, JSON, Preise)."""
import requests, re, random
from .smart_crawl import rotate_user_agent, _load, _save, _dom
from .router import ask_router
from .gitAG import auto_commit

def data_crawl(command: str) -> str:
    """Extrahiert strukturierte Daten aus einer URL."""
    try:
        resp = ask_router(command, "Extrahiere nur die reine URL. Kein Zusatztext.", agent_name="data_crawlerAG")
        url = resp.strip()
        if not url.startswith("http"):
            return "❌ Keine valide URL gefunden."
        headers = {"User-Agent": rotate_user_agent(), "Accept": "application/json, text/html, */*"}
        r = requests.get(url, timeout=20, headers=headers)
        db, dom = _load(), _dom(url)
        db.setdefault(dom, {"blocks": 0, "last": 0})
        import time; db[dom]["last"] = time.time()
        _save(db)
        html = r.text[:12000]
        result = ask_router(
            f"URL: {url}\nHTML: {html}",
            "Extrahiere alle strukturierten Daten (Tabellen, Listen, Preise, JSON). Gib sauberes Ergebnis.",
            agent_name="data_crawlerAG"
        )
        auto_commit(".")
        return result
    except Exception as e:
        return f"❌ Data-Crawl Fehler: {str(e)}"
