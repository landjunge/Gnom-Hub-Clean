from typing import Dict, Tuple
class SmartRouter:
    STAGES: Dict[str, Tuple[int, str, str]] = {
        "stage_1": (1, "free", "fast"),
        "stage_2": (2, "free", "medium"),
        "stage_3": (3, "cheap", "balanced"),
        "stage_4": (4, "premium", "high"),
    }
    ROLE_PREFERENCE = {"coder": "stage_4", "security": "stage_4", "normal": "stage_3", "brainstorm": "stage_2"}
    @staticmethod
    def get_stage_for_role(role: str) -> str:
        return SmartRouter.ROLE_PREFERENCE.get(role.lower(), "stage_3")
    @staticmethod
    def get_best_model(stage: str, available_models: list) -> str:
        preferred = {
            "stage_4": ["claude-3.5-sonnet", "gpt-4o", "deepseek-reasoner"],
            "stage_3": ["gpt-4o-mini", "mistral-large", "llama3.1"],
            "stage_2": ["llama3.2", "gemma2"],
            "stage_1": ["llama3.2", "phi3"],
        }.get(stage, ["llama3.2"])
        for m in preferred:
            if any(m.lower() in am.lower() for am in available_models): return m
        return available_models[0] if available_models else "llama3.2"

def is_valid(provider, kdb):
    return any(k.get("provider") == provider and k.get("valid") for k in kdb.values())

def resolve_stage(stage, kdb, agent_name):
    role = "coder" if "coder" in agent_name.lower() else "normal"
    for pvd, mdl in get_stage_options(stage, role):
        if pvd == "lokal" or is_valid(pvd, kdb): return pvd, mdl
    return "lokal", "llama3"

def get_stage_options(stage, role):
    s4 = [("anthropic", "claude-3-5-sonnet-20241022"), ("openai", "gpt-4o"), ("gemini", "gemini-1.5-pro"), ("deepseek", "deepseek-chat")]
    s3 = [("deepseek", "deepseek-chat"), ("gemini", "gemini-1.5-flash"), ("openrouter", "qwen/qwen3-coder:free" if role == "coder" else "meta-llama/llama-3.3-70b-instruct:free"), ("openai", "gpt-4o-mini"), ("mistral", "mistral-large-latest")]
    s2 = [("openrouter", "qwen/qwen3-coder:free" if role == "coder" else "meta-llama/llama-3.3-70b-instruct:free")]
    s1 = [("lokal", "llama3"), ("lokal", "llama3.2"), ("lokal", "mistral")]
    return (s4 + s3 + s2 + s1) if stage == "stage_4" else ((s3 + s2 + s1) if stage == "stage_3" else ((s2 + s1) if stage == "stage_2" else s1))
