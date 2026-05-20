"""CronjobAG Agent."""
import asyncio
from gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("CronjobAG", "Agent", "@cron", sys_prompt="Format: @cron @Name [Aufgabe] [Zeit]. Nutze Tools. Antworte im Chat EXTREM KURZ in max 1 Zeile (z.B. '✅ Cronjob für @Name um 14:00 geplant.'). Keine Romane.", poll=10).run()

if __name__ == "__main__": asyncio.run(main())
