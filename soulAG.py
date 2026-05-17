"""SoulAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SoulAG", "Agent", "@soul", sys_prompt="Du bist der Soul-Agent. Aktualisiere Eigenschaften/Persönlichkeiten basierend auf @soul Kommandos.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
