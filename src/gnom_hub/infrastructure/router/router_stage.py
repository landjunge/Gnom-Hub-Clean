from typing import Dict, Tuple
from ...core.config import Config

class SmartRouter:
    """Kostenoptimiertes Auto-Routing: DeepSeek erlaubt, Claude Sonnet/Opus verboten."""
    STAGES: Dict[str, Tuple[int, str, str]] = {
        "stage_1": (1, "free", "fast"), "stage_2": (2, "free", "medium"),
        "stage_3": (3, "cheap", "balanced"), "stage_4": (4, "premium", "high")
    }
    ROLE_PREFERENCE = {
        "coder": "stage_4",  # Darf DeepSeek Reasoner nutzen
        "security": "stage_3", "normal": "stage_3",
        "brainstorm": "stage_2", "default": "stage_3"
    }
    FORBIDDEN_MODELS = {"claude-3.5-sonnet", "claude-opus", "claude-3-opus"}  # Verbotene teure Modelle

    @staticmethod
    def get_stage_for_role(role: str) -> str:
        return SmartRouter.ROLE_PREFERENCE.get(role.lower(), "stage_3")

    @staticmethod
    def get_best_model(stage: str, available_models: list) -> str:
        """Bevorzugt DeepSeek, ignoriert Claude Sonnet/Opus."""
        preferred = {
            "stage_4": ["deepseek-reasoner", "deepseek-chat", "gpt-4o-mini", "mistral-large"],
            "stage_3": ["deepseek-chat", "llama3.1", "mistral-large", "gpt-4o-mini"],
            "stage_2": ["llama3.2", "gemma2"], "stage_1": ["llama3.2", "phi3"]
        }.get(stage, ["llama3.2"])
        for model in preferred:
            model_lower = model.lower()
            if any(f in model_lower for f in SmartRouter.FORBIDDEN_MODELS):
                continue  # Claude-Modelle überspringen
            if any(model_lower in m.lower() for m in available_models):
                return model
        for m in available_models:  # Fallback: erstes verfügbares (nicht verboten)
            if not any(f in m.lower() for f in SmartRouter.FORBIDDEN_MODELS):
                return m
        return "llama3.2"
