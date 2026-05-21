"""ResearcherAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("ResearcherAG", "Deep research and fact-finding", "@research", sys_prompt="SYSTEM-ROLLE: RESEARCHER. Deep research, verify facts, cite sources.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
