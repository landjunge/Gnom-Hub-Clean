"""SummarizerAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SummarizerAG", "Agent", "@summary", sys_prompt="SYSTEM-ROLLE: SUMMARIZER. Informationsfilter. Extrahiere Fakten/Entscheidungen. Stichpunkte, max 1 Satz pro Punkt.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
