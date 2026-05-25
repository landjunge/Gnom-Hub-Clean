from ...core.config import Config
from ..router.router_stage import SmartRouter
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.infrastructure.database.agent_repo import SQLiteAgentRepository

class KeyAssigner:
    @staticmethod
    async def assign_for_agent(agent_role: str, available_providers: list) -> dict:
        stage = SmartRouter.get_stage_for_role(agent_role)
        pref = Config.DEFAULT_LLM_PROVIDER
        if pref not in available_providers:
            pref = "ollama" if "ollama" in available_providers else (available_providers[0] if available_providers else "ollama")
        model = SmartRouter.get_best_model(stage, ["llama3", "claude-3.5-sonnet", "gpt-4o-mini"])
        return {"provider": pref, "model": model, "stage": stage, "reason": f"Rolle '{agent_role}' -> Stufe {stage}"}

async def auto_assign_keys():
    db, rep = SQLiteStateRepository(), SQLiteAgentRepository()
    agents, maps = rep.get_all(), {}
    for a in agents:
        role = a.role or "normal"
        stage = SmartRouter.get_stage_for_role(role)
        maps[a.name.lower()] = {"provider": "auto", "model": stage}
    db.set_value("llm_agents", maps)
