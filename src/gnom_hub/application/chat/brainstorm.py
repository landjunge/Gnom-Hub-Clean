import asyncio
from uuid import UUID
from typing import List
from ...domain.chat.entities import ChatMessage
from ...domain.agent.repository import AgentRepository
from ...infrastructure.llm.orchestrator import LLMOrchestrator

class BrainstormUseCase:
    """Use Case: Paralleles Brainstorming mit mehreren Agenten."""

    def __init__(self, agent_repo: AgentRepository, llm_orchestrator: LLMOrchestrator):
        self.agent_repo = agent_repo
        self.llm_orchestrator = llm_orchestrator

    async def execute(self, agent_ids: List[UUID], topic: str, rounds: int = 3) -> List[ChatMessage]:
        """Führt ein paralleles Brainstorming durch und gibt alle Antworten zurück."""
        messages: List[ChatMessage] = []
        agents = [await self.agent_repo.get_by_id(aid) for aid in agent_ids]
        
        for round_num in range(rounds):
            round_responses = []
            for a in agents:
                if a:
                    res = await self.llm_orchestrator.ask(
                        agent_id=str(a.id),
                        prompt=f"Runde {round_num+1}: {topic}",
                        model=a.model
                    )
                    round_responses.append(res)

            for i, response in enumerate(round_responses):
                msg = ChatMessage(
                    agent_id=agents[i].id,
                    role="assistant",
                    content=response,
                    model=agents[i].model or "brainstorm"
                )
                messages.append(msg)

        return messages
