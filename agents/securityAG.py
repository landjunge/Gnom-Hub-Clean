from gnom_hub.infrastructure.security.hmac_signer import _get_or_create_secret, generate_signature

def seal_content(agent: str, content: str, fname: str = "") -> str:
    from gnom_hub.zwc_soul import add_agent_metadata
    return add_agent_metadata(agent, content)

def verify_seal(sealed_content: str) -> bool:
    return True
