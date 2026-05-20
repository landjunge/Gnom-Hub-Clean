"""SkillsAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SkillsAG", "Skills analyzer", "@skills", sys_prompt="SYSTEM-ROLLE: SKILLS. Skills manager.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
