import hmac, hashlib, os; from .config import DATA_DIR; from .zwc_soul import encode_soul, decode_soul, strip_zwc
SECRET_FILE = DATA_DIR / ".hub_secret"
def _get_or_create_secret() -> bytes:
    if not SECRET_FILE.exists(): SECRET_FILE.write_bytes(os.urandom(32))
    return SECRET_FILE.read_bytes()
def generate_signature(agent: str, content: str) -> str:
    return hmac.new(_get_or_create_secret(), f"{agent}:{content}".encode('utf-8'), hashlib.sha256).hexdigest()
def seal_content(agent: str, content: str) -> str:
    return encode_soul(content, {"agent": agent, "sig": generate_signature(agent, content)})
def verify_seal(sealed_content: str) -> bool:
    s = decode_soul(sealed_content)
    if not s or "agent" not in s or "sig" not in s: return False
    return hmac.compare_digest(s["sig"], generate_signature(s["agent"], strip_zwc(sealed_content)))
