from typing import Optional
from gnom_hub.domain.agent.repository import AgentRepository

class SyncAgentStatus:
    def __init__(self, repo: AgentRepository):
        self.repo = repo

    def execute(self, name_or_id: str, status: str, active_job: Optional[str] = None) -> None:
        agent = self.repo.get_by_id(name_or_id)
        if not agent:
            raise ValueError(f"Agent {name_or_id} not found")
        self.repo.update_status(agent.name, status, active_job)
