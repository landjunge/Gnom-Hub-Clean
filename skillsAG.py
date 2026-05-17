"""SkillsAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SkillsAG", "Agent", "@skill", sys_prompt="Du bist der Skills-Agent. Verwalte neue Fähigkeiten.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
