from . import (
    memory_crud, memory_search, agents_list, agents_status, nudge, registry,
    chat, audio, admin_tools, admin_system, admin_config, workspace,
    llm_keys, llm_agents, llm_models, system_info, showbox, agents, admin
)

routers = [
    memory_crud.router, memory_search.router, agents_list.router, agents_status.router,
    nudge.router, registry.router, chat.router, audio.router, admin_tools.router,
    admin_system.router, admin_config.router, workspace.router, llm_keys.router,
    llm_agents.router, llm_models.router, system_info.router, showbox.router, agents.router, admin.router
]
