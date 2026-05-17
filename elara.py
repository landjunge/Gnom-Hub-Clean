"""Elara — Code-Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("Elara", "LLM Test-Agent", "@elara").run()

if __name__ == "__main__": asyncio.run(main())
