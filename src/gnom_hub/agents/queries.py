from typing import List
from uuid import UUID
from gnom_hub.agents.entities import Agent
from gnom_hub.db.agent_repo import AgentRepository


class AgentQueries:
    """Queries für Leseoperationen auf Agenten."""

    def __init__(self, agent_repo: AgentRepository):
        self.agent_repo = agent_repo

    async def get_agent(self, agent_id: UUID) -> Agent:
        """Lädt einen einzelnen Agenten."""
        agent = await self.agent_repo.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent mit ID {agent_id} nicht gefunden")
        return agent

    async def list_agents(self) -> List[Agent]:
        """Gibt alle Agenten zurück."""
        return await self.agent_repo.list_all()

    async def get_running_agents(self) -> List[Agent]:
        """Gibt nur laufende Agenten zurück."""
        agents = await self.agent_repo.list_all()
        return [a for a in agents if a.is_running()]
