from typing import Dict, Tuple

class SmartRouter:
    """Kostenoptimiertes Auto-Routing – keine teuren Modelle (max. Stage 3)."""
    STAGES: Dict[str, Tuple[int, str, str]] = {
        "stage_1": (1, "free", "fast"),
        "stage_2": (2, "free", "medium"),
        "stage_3": (3, "cheap", "balanced"),
    }
    ROLE_PREFERENCE = {
        "coder": "stage_3",
        "security": "stage_3",
        "normal": "stage_3",
        "brainstorm": "stage_2",
        "default": "stage_3",
    }
    @staticmethod
    def get_stage_for_role(role: str) -> str:
        """Gibt immer eine günstige Stufe zurück (max. Stage 3)."""
        return SmartRouter.ROLE_PREFERENCE.get(role.lower(), "stage_3")
    @staticmethod
    def get_best_model(stage: str, available_models: list) -> str:
        """Wählt nur günstige / lokale Modelle."""
        preferred = {
            "stage_3": ["llama3.1", "llama3", "mistral-large", "gemma2"],
            "stage_2": ["llama3.2", "gemma2"],
            "stage_1": ["llama3.2", "phi3"],
        }.get(stage, ["llama3.2"])
        for model in preferred:
            if any(model.lower() in m.lower() for m in available_models): return model
        return available_models[0] if available_models else "llama3.2"
