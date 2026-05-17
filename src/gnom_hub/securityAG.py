import hmac
import hashlib
import os
from .config import DATA_DIR
from .zwc_soul import encode_soul, decode_soul

SECRET_FILE = DATA_DIR / ".hub_secret"

def _get_or_create_secret() -> bytes:
    if not SECRET_FILE.exists():
        SECRET_FILE.write_bytes(os.urandom(32))
    return SECRET_FILE.read_bytes()

def generate_signature(agent_name: str, content: str) -> str:
    """Generiert einen HMAC-SHA256 über Content + AgentName."""
    secret = _get_or_create_secret()
    # Wir signieren den eigentlichen Inhalt
    message = f"{agent_name}:{content}".encode('utf-8')
    sig = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return sig

def seal_content(agent_name: str, content: str) -> str:
    """Erstellt das ZWC-Siegel und hängt es an den Content."""
    sig = generate_signature(agent_name, content)
    soul_dict = {"agent": agent_name, "sig": sig}
    return encode_soul(content, soul_dict)

def verify_seal(sealed_content: str) -> bool:
    """Extrahiert das ZWC-Siegel und verifiziert die Signatur."""
    soul = decode_soul(sealed_content)
    if not soul or "agent" not in soul or "sig" not in soul:
        return False
    
    agent_name = soul["agent"]
    sig = soul["sig"]
    
    # Der ZWC Payload muss vom Content abgezogen werden, um die Signatur zu prüfen
    from .zwc_soul import strip_zwc
    pure_content = strip_zwc(sealed_content)
    
    expected_sig = generate_signature(agent_name, pure_content)
    return hmac.compare_digest(sig, expected_sig)
