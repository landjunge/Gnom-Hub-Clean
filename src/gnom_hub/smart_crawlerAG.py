from .smart_crawl import smart_request
from .router import ask_router

def smart_crawl(command: str) -> str:
    """Haupteinstiegspunkt für generalAG."""
    try:
        resp = ask_router(command, "Extrahiere nur die URL aus dem Befehl. Gib NUR die URL zurück.", agent_name="smart_crawlerAG")
        url = resp.strip()
        if not url.startswith("http"): return "❌ Keine valide URL gefunden."
        return smart_request(url)
    except:
        return "❌ Crawl fehlgeschlagen."
