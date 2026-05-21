"""WriterAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("WriterAG", "Content creation and text drafting", "@write", sys_prompt="SYSTEM-ROLLE: WRITER. Draft clear, structured content. No filler.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
