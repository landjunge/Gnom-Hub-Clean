"""WatchdogAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent(
        "WatchdogAG",
        "Workspace integrity check",
        "@watchdog",
        sys_prompt="SYSTEM-ROLLE: WATCHDOG. Überwache die Sicherheit und Integrität des Workspace.",
        poll=15
    ).run()

if __name__ == "__main__":
    asyncio.run(main())
