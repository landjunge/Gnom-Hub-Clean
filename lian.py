"""Lian Agent."""
import asyncio
from src.gnom_hub.agent_base import BaseAgent

async def main():
    await BaseAgent("Lian", "Agent", "@lian", sys_prompt="Du bist ein technischer Code-Agent. Kein Rollenspiel, keine Motivation, keine Philosophie. Analysiere das Problem, schreibe den Code und nutze deine Tools, um ihn sofort auszuführen oder zu deployen. Antworte extrem kurz und direkt.", poll=15).run()

if __name__ == "__main__": asyncio.run(main())
