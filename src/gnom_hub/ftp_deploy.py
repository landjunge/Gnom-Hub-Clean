import os, json, ftplib, re; from pathlib import Path
from agents.securityAG import seal_content; from gnom_hub.zwc_soul import strip_zwc
from .config import DATA_DIR
def get_deploy():
    p = DATA_DIR / "state.json"
    try: return json.load(open(p, "r", encoding="utf-8")).get("auto_deploy", False)
    except: return False
def set_deploy(val):
    p = DATA_DIR / "state.json"
    s = json.load(open(p, "r", encoding="utf-8")) if p.exists() else {}
    s["auto_deploy"] = val
    json.dump(s, open(p, "w", encoding="utf-8"), indent=2)
def upload(local, remote):
    try:
        with ftplib.FTP("185.243.11.43", timeout=10) as ftp:
            ftp.login("sysuser_a", "5Rdv4uH6~Owlqn~k")
            ftp.cwd("netzwerkpunkt.de/httpdocs")
            with open(local, "rb") as f: ftp.storbinary(f"STOR {remote}", f)
    except Exception as e: print("[FTP] Error:", e)
def sync_index(wd):
    wd = Path(wd); idx = wd / "index.html"
    if not idx.exists(): return
    files = [f for f in os.listdir(wd) if f.endswith((".html", ".md")) and f != "index.html" and not f.startswith(".")]
    cards = []
    for f in sorted(files):
        ext = f.split(".")[-1]; t = f.replace(f".{ext}", "").replace("_", " ").title()
        i = "🏠" if "landing" in f else ("⚡" if ext == "html" else "📘")
        c = "html" if ext == "html" else "md"
        cards.append(f'<a href="{f}" class="card {c}" target="_blank"><div class="icon">{i}</div><div class="title">{t}</div><div class="desc">{t} Seite.</div><span class="tag {c}-tag">{ext.upper()}</span></a>')
    html = re.sub(r'(<div class="grid">)(.*?)(</div>)', r'\1\n        ' + "\n        ".join(cards) + r'\n    \3', strip_zwc(idx.read_text(encoding="utf-8")), flags=re.DOTALL)
    idx.write_text(seal_content("System", html, "index.html"), encoding="utf-8")
    upload(idx, "index.html")
    for f in files: upload(wd / f, f)
