"""SecurityAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SecurityAG", "Agent", "@security", sys_prompt="Du bist der Security-Agent. Prüfe Logs und API-Keys.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
