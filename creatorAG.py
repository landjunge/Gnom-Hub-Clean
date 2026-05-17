"""CreatorAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("CreatorAG", "Agent", "@creator", sys_prompt="Du bist ein Generator für neue Agenten.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
