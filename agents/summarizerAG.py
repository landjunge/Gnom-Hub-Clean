"""SummarizerAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("SummarizerAG", "Condense information", "@summarize", sys_prompt="SYSTEM-ROLLE: SUMMARIZER. Condense info to the absolute minimum.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
