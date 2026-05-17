"""Crawler-Engine: Dispatch auf die 3 Crawl-Strategien."""
import re, json, random, requests, time
from .smart_crawl import smart_request, rotate_user_agent, _load, _save, _dom

def crawl_simple(url, timeout=15):
    """web_crawlerAG: Einfacher Crawl, ein UA, kein Memory."""
    r = requests.get(url, timeout=timeout, headers={"User-Agent": rotate_user_agent()})
    t = re.sub(r'<[^>]+>', ' ', r.text)
    return re.sub(r'\s+', ' ', t).strip()[:3000]

def crawl_smart(url, timeout=20):
    """smart_crawlerAG: Anti-Block via smart_crawl Modul."""
    return smart_request(url)

def crawl_data(url, timeout=20):
    """data_crawlerAG: Strukturierte Daten extrahieren."""
    time.sleep(random.uniform(1.0, 2.5))
    h = {"User-Agent": rotate_user_agent(), "Accept": "application/json, text/html, */*"}
    try:
        r = requests.get(url, timeout=timeout, headers=h)
        db, dom = _load(), _dom(url)
        db.setdefault(dom, {"blocks": 0, "last": 0})["last"] = time.time()
        _save(db)
        ct = r.headers.get("Content-Type", "")
        if "json" in ct:
            return json.dumps(r.json(), indent=2, ensure_ascii=False)[:3000]
        html = r.text
        tables = re.findall(r'<table.*?</table>', html, re.DOTALL)
        lists = re.findall(r'<(?:ul|ol).*?</(?:ul|ol)>', html, re.DOTALL)
        result = ""
        for t in tables[:3]:
            c = re.sub(r'<[^>]+>', ' | ', t)
            result += re.sub(r'\s+', ' ', c).strip() + "\n\n"
        for l in lists[:5]:
            c = re.sub(r'<li[^>]*>', '• ', l)
            c = re.sub(r'<[^>]+>', '', c)
            result += re.sub(r'\s+', ' ', c).strip() + "\n"
        if not result.strip():
            t = re.sub(r'<[^>]+>', ' ', html)
            result = re.sub(r'\s+', ' ', t).strip()
        return result[:3000]
    except Exception as e:
        return f"[DATA-FEHLER] {str(e)[:100]}"

