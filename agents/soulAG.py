"""SoulAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SoulAG", "Swarm consciousness", "@soul", sys_prompt="SYSTEM-ROLLE: SOUL. Swarm consciousness and controller.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
