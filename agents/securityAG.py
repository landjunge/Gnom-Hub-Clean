import hmac, hashlib, os, re, json; from gnom_hub.config import DATA_DIR; from gnom_hub.zwc_soul import encode_soul, decode_soul, strip_zwc
SECRET_FILE = DATA_DIR / ".hub_secret"
def _get_or_create_secret() -> bytes:
    if not SECRET_FILE.exists(): SECRET_FILE.write_bytes(os.urandom(32))
    return SECRET_FILE.read_bytes()
def generate_signature(agent: str, content: str) -> str:
    return hmac.new(_get_or_create_secret(), f"{agent}:{content}".encode('utf-8'), hashlib.sha256).hexdigest()
def seal_content(agent: str, content: str, fname: str = "") -> str:
    ext = os.path.splitext(fname)[1].lower() if fname else ""
    pre, suf = "", ""
    if ext == ".py": pre = "\n# "
    elif ext in (".js", ".css"): pre, suf = "\n/* ", " */"
    elif ext in (".html", ".xml"): pre, suf = "\n<!-- ", " -->"
    payload = {"agent": agent}
    if agent.lower() == "soulag":
        m = re.search(r"(\{.*?\})", content, re.DOTALL)
        if m:
            try:
                data = json.loads(m.group(1))
                if isinstance(data, dict):
                    if "name" not in data: data["name"] = "user_soul"
                    payload.update(data)
            except: pass
    base = content + pre
    payload["sig"] = generate_signature(agent, base + suf)
    return encode_soul(base, payload) + suf
def verify_seal(sealed_content: str) -> bool:
    s = decode_soul(sealed_content)
    if not s or "agent" not in s or "sig" not in s: return False
    return hmac.compare_digest(s["sig"], generate_signature(s["agent"], strip_zwc(sealed_content)))
