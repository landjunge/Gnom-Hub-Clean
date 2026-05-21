"""EditorAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("EditorAG", "Review, refine and quality-check text", "@edit", sys_prompt="SYSTEM-ROLLE: EDITOR. Review, refine and fix text. Return corrected version only.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
