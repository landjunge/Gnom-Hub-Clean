import httpx, asyncio

async def verify_key(provider: str, key: str) -> dict:
    headers = {"Authorization": f"Bearer {key}"}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if provider == "deepseek":
                r = await client.get("https://api.deepseek.com/user/balance", headers=headers)
                return {"valid": r.status_code == 200, "info": "OK" if r.status_code == 200 else r.text, "caps": ["text", "tools"]}
            if provider == "openrouter":
                r = await client.get("https://openrouter.ai/api/v1/auth/key", headers=headers)
                return {"valid": r.status_code == 200, "info": "OK" if r.status_code == 200 else r.text, "caps": ["text", "vision", "tools"]}
            if provider == "openai":
                r = await client.get("https://api.openai.com/v1/models", headers=headers)
                return {"valid": r.status_code == 200, "info": "OK" if r.status_code == 200 else r.text, "caps": ["text", "vision", "image", "audio", "tools"]}
            if provider == "anthropic":
                r = await client.get("https://api.anthropic.com/v1/models", headers={"x-api-key": key, "anthropic-version": "2023-06-01"})
                return {"valid": r.status_code == 200, "info": "OK" if r.status_code == 200 else r.text, "caps": ["text", "vision", "tools"]}
            if provider == "gemini":
                r = await client.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}")
                return {"valid": r.status_code == 200, "info": "OK" if r.status_code == 200 else r.text, "caps": ["text", "vision", "image", "audio", "tools"]}
            if provider == "mistral":
                r = await client.get("https://api.mistral.ai/v1/models", headers=headers)
                return {"valid": r.status_code == 200, "info": "OK" if r.status_code == 200 else r.text, "caps": ["text", "vision", "tools"]}
    except Exception as e:
        return {"valid": False, "info": str(e), "caps": []}
    return {"valid": False, "info": "Unknown provider", "caps": []}

async def auto_detect_and_verify(key: str) -> dict:
    if key.startswith("sk-or-"): return {**await verify_key("openrouter", key), "provider": "openrouter"}
    if key.startswith("sk-ant-"): return {**await verify_key("anthropic", key), "provider": "anthropic"}
    if key.startswith("AIzaSy"): return {**await verify_key("gemini", key), "provider": "gemini"}
    if key.startswith("sk-"):
        res = await asyncio.gather(verify_key("deepseek", key), verify_key("openai", key), verify_key("mistral", key), return_exceptions=True)
        for p, r in zip(["deepseek", "openai", "mistral"], res):
            if isinstance(r, dict) and r.get("valid"): return {**r, "provider": p}
    return {"valid": False, "info": "Kein bekannter Provider erkannt", "caps": []}
