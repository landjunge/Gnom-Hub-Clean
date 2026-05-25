# swarm_coordinator.py — Coordinates team workflows and gathers results
import time, threading
from gnom_hub.infrastructure.database.agent_repo import SQLiteAgentRepository
from gnom_hub.infrastructure.database.state_repo import SQLiteStateRepository
from gnom_hub.role_tools import _llm
from gnom_hub.brainstorm import _collect_worker_responses
from gnom_hub.brainstorm_helpers import post, get_workspace_dir
from gnom_hub.action_handlers import process_actions
from gnom_hub.soul_initializer import get_soul

def run_swarm_coordinator(task, workers):
    agent_repo = SQLiteAgentRepository()
    time.sleep(5)
    for _ in range(60):
        time.sleep(2)
        active = [a for a in agent_repo.get_all() if a.name in workers]
        if not any(a.active_job for a in active): break
    responses = _collect_worker_responses(workers)
    sys_p = "Du bist GeneralAG. Führe die Ergebnisse des Team-Workflows zusammen und erstelle ein fertiges Dokument/Code im Format [WRITE: dateiname]inhalt[/WRITE]."
    ans = _llm(sys_p, f"Job: {task}\n\nErgebnisse:\n{responses}")
    gen = next((a for a in agent_repo.get_all() if a.role == "general" or a.name.lower() == "generalag"), None)
    if gen:
        soul = get_soul(gen.name) or {}
        post(gen.name, process_actions(ans, {"name": gen.name}, soul.get("permissions", []), False, get_workspace_dir()))
    SQLiteStateRepository().set_value("active_workflow", None)

def start_coordinator(task, workers):
    if workers:
        SQLiteStateRepository().set_value("active_workflow", f"Team-Workflow aktiv: {' → '.join(workers)}")
        threading.Thread(target=run_swarm_coordinator, args=(task, workers), daemon=True).start()
