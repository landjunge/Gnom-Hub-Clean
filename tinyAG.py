"""TinyAG Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("TinyAG", "Agent", "@tiny", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
