"""CoderAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("CoderAG", "Code generation and technical implementation", "@code", sys_prompt="SYSTEM-ROLLE: CODER. Write clean, working code. Prefer simple solutions.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
