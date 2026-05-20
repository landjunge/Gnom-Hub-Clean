"""GeneralAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("GeneralAG", "Agent", "@job", sys_prompt="SYSTEM-ROLLE: GENERAL. Task-Distributions-Maschine. Analysiere @job und verteile Aufgaben via @Name -> Aufgabe. Keine Erklärungen.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
