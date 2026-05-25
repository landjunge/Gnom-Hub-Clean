from ...core.config import Config


class SmartRouter:
    """Kostenoptimiertes Auto-Routing – verwendet nur die zentrale Liste aus Config."""

    ROLE_PREFERENCE = {
        "coder": "stage_3",
        "security": "stage_3",
        "normal": "stage_3",
        "brainstorm": "stage_2",
        "default": "stage_3",
    }

    @staticmethod
    def get_stage_for_role(role: str) -> str:
        return SmartRouter.ROLE_PREFERENCE.get(role.lower(), "stage_3")

    @staticmethod
    def get_best_model(stage: str, available_models: list) -> str:
        """Nutzt die zentrale Free-Liste aus Config."""
        preferred_order = Config.OPENROUTER_FREE_MODELS

        for model in preferred_order:
            if any(model.lower() in m.lower() for m in available_models):
                return model

        return available_models[0] if available_models else "llama3.2"
