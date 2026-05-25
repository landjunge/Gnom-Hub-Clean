import httpx
from typing import Optional
from ...core.config import Config
from ...common.exceptions import LLMProviderError

class OpenRouterClient:
    """Client für OpenRouter API – optimiert für Free-Tier-Modelle."""

    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        if not self.api_key:
            raise LLMProviderError("OPENROUTER_API_KEY ist nicht gesetzt")

    async def ask(self, prompt: str, model: Optional[str] = None) -> str:
        """Sendet eine Prompt-Anfrage. Verwendet das vom SmartRouter übergebene Modell."""
        # Fallback auf ein günstiges Modell, falls keines übergeben wurde
        final_model = model or "meta-llama/llama-3.1-8b-instruct"
        headers = {"Authorization": f"Bearer {self.api_key}", "HTTP-Referer": "http://localhost:8000", "X-Title": "Gnom-Hub"}
        payload = {"model": final_model, "messages": [{"role": "user", "content": prompt}]}
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                raise LLMProviderError(f"OpenRouter-Anfrage fehlgeschlagen: {e}") from e
