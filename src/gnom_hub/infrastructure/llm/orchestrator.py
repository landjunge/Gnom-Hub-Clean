import asyncio
from typing import List, Optional
from ...domain.chat.entities import ChatMessage
from ...router import ask_router
from ...infrastructure.database.agent_repo import SQLiteAgentRepository

class LLMOrchestrator:
    async def ask(self, agent_id: str, prompt: str, model: Optional[str] = None) -> str:
        repo = SQLiteAgentRepository()
        try:
            agent = await repo.get_by_id(agent_id)
        except Exception:
            agent = await repo.get_by_name(agent_id)
        name = agent.name if agent else agent_id
        sys = agent.description if agent else "Du bist ein Assistent."
        
        loop = asyncio.get_running_loop()
        ans = await loop.run_in_executor(None, ask_router, prompt, sys, name)
        return ans

    async def generate_response(self, agent_id: str, messages: List[ChatMessage]) -> str:
        return await self.ask(agent_id, messages[-1].content if messages else "")
