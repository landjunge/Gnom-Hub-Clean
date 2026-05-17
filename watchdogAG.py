"""WatchdogAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("WatchdogAG", "Agent", "@watchdog", sys_prompt="Du bist der Watchdog. Prüfe System-Gesundheit auf @watchdog. Antworte kurz: STATUS | RAM | AGENTS.", poll=10).run()

if __name__ == "__main__": asyncio.run(main())
