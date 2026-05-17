"""smart_crawlerAG: Anti-Block-Logik mit Domain-Memory."""
import os, json, time, random, requests, re
from urllib.parse import urlparse

DB = os.path.join(os.path.dirname(__file__), "../../.gnom-hub-domains.json")
UA = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Firefox/128.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64) Firefox/127.0",
]

def _mem():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def _save(d):
    json.dump(d, open(DB, "w"), indent=2)

def _dom(url):
    return urlparse(url).netloc

def rotate_user_agent():
    return random.choice(UA)

def get_random_delay(blocks=0):
    base = random.uniform(1.2, 4.5)
    return base * min(1 + blocks * 0.8, 10)

def check_for_block(r):
    if r.status_code in (403, 429, 503): return True
    s = ["cloudflare", "captcha", "cf-browser", "access denied"]
    return any(x in r.text[:2000].lower() for x in s)

def smart_request(url):
    dom, db = _dom(url), _mem()
    info = db.get(dom, {"blocks": 0, "last": 0})
    time.sleep(get_random_delay(info["blocks"]))
    h = {"User-Agent": rotate_user_agent(), "Accept": "text/html,*/*",
         "Accept-Language": "de,en;q=0.5", "Referer": f"https://google.com/search?q={dom}", "DNT": "1"}
    try:
        r = requests.get(url, timeout=20, headers=h)
        info["last"] = time.time()
        if check_for_block(r):
            info["blocks"] = info.get("blocks", 0) + 1
            db[dom] = info; _save(db)
            if info["blocks"] >= 3:
                return f"[BLOCK×{info['blocks']}] {dom} — Fallback: ultra-slow"
            return f"[BLOCK] {dom} (Status {r.status_code}, #{info['blocks']})"
        if info["blocks"] > 0: info["blocks"] -= 1
        db[dom] = info; _save(db)
        t = re.sub(r'<[^>]+>', ' ', r.text)
        return re.sub(r'\s+', ' ', t).strip()[:3000]
    except Exception as e:
        return f"[FEHLER] {str(e)[:100]}"
