from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.infrastructure.database.agent_repo import SQLiteAgentRepository

async def auto_assign_keys():
    kdb = SQLiteStateRepository().get_value("llm_keys", {})
    valid_providers = {k.get("provider") for k in kdb.values() if k.get("valid")}
    
    mappings = {}
    agents = SQLiteAgentRepository().get_all()
    
    for a in agents:
        role = a.role or "normal"
        name = a.name.lower()
        
        if "anthropic" in valid_providers and (role == "coder" or "coder" in name):
            p, m = "anthropic", "claude-3-5-sonnet-20241022"
        elif "openai" in valid_providers:
            p, m = "openai", "gpt-4o"
        elif "deepseek" in valid_providers:
            p, m = "deepseek", "deepseek-chat"
        elif "gemini" in valid_providers:
            p, m = "gemini", "gemini-1.5-pro"
        elif "openrouter" in valid_providers:
            if "coder" in name or role == "coder":
                p, m = "openrouter", "qwen/qwen3-coder:free"
            else:
                p, m = "openrouter", "deepseek/deepseek-v4-flash:free"
        else:
            p, m = "lokal", "llama3"
            
        mappings[a.name.lower()] = {"provider": p, "model": m}
        
    SQLiteStateRepository().set_value("llm_agents", mappings)
