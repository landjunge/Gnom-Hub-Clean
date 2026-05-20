import re; from pathlib import Path; from .provider_switchAG import llm_call; from .gitAG import auto_commit, git_cmd; from .sandboxAG import safe_run_command
def evolve_agent(name: str) -> str:
    h = git_cmd(".", "log --oneline -5")
    try: l = Path(".backups/sandbox.log").read_text()[-500:]
    except: l = "Keine Logs vorhanden."
    p = f"Agent: {name}\nLogs: {l}\nGit: {h}\nSchreibe verbesserten Code für {name}.py.\nRegeln:\n- Max 40 Zeilen!\n- Nur nötige Imports.\n- NUR roher Python-Code ohne Fences."
    try:
        c = re.sub(r'```(?:python)?\s*|\s*```', '', llm_call(p, system="Du bist der Evolution-Agent. Output ist ausschließlich roher Python-Code."), flags=re.DOTALL).strip()
        f = Path(__file__).parent / f"{name}.py"; f.write_text(c); auto_commit(".", message=f"Evolution: {name} self-improved")
        return f"✅ {name} evolviert – neuer Code in {f.name} committed!"
    except Exception as e:
        safe_run_command(f"echo 'Evolution Error: {str(e)}' >> .backups/sandbox.log", "evolutionAG")
        return f"❌ Evolution fehlgeschlagen: {str(e)}"
