import os

replacements = {
    "gnom_hub.infrastructure.database.state_repo": "gnom_hub.db.state_repo",
    "gnom_hub.infrastructure.database.agent_repo": "gnom_hub.db.agent_repo",
    "gnom_hub.infrastructure.database.chat_repo": "gnom_hub.db.chat_repo",
    "gnom_hub.infrastructure.database.agent_role": "gnom_hub.db.agent_role",
    "gnom_hub.infrastructure.database": "gnom_hub.db"
}

files = [
    "src/gnom_hub/api/endpoints/admin_config.py",
    "src/gnom_hub/api/endpoints/admin_system.py",
    "src/gnom_hub/api/endpoints/admin_tools.py",
    "src/gnom_hub/api/endpoints/agents_list.py",
    "src/gnom_hub/api/endpoints/audio.py",
    "src/gnom_hub/api/endpoints/chat_helpers.py",
    "src/gnom_hub/api/endpoints/llm_agents.py",
    "src/gnom_hub/api/endpoints/llm_models.py",
    "src/gnom_hub/api/endpoints/nudge.py",
    "src/gnom_hub/api/endpoints/workspace.py",
    "src/gnom_hub/chat/chat_commands.py",
    "src/gnom_hub/infrastructure/llm/desktop_syncer.py",
    "src/gnom_hub/infrastructure/router/llm_orchestrator.py",
    "src/gnom_hub/infrastructure/router/router_stage.py"
]

for f_path in files:
    full_path = os.path.join("/Users/landjunge/Documents/AG-Flega", f_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        orig = content
        for k, v in replacements.items():
            content = content.replace(k, v)
        
        if content != orig:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {f_path}")
