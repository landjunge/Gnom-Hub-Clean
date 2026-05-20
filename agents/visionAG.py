import pyautogui, time, re, json, pathlib; from .provider_switchAG import llm_call; from .gitAG import auto_commit; from .evaluatorAG import evaluate_job; from .sandboxAG import safe_run_command
V_DIR = pathlib.Path(".visions"); V_DIR.mkdir(parents=True, exist_ok=True)
def _val(d): return isinstance(d, dict) and all(k in d and (isinstance(d[k], str) if v==str else (d[k] in v if isinstance(v, list) else any(isinstance(d[k], t) for t in v))) for k,v in {"description": str, "action": ["click", "type", "scroll", "move", "done"], "params": (str, int, list, type(None))}.items())
def vision_loop(cmd: str, max_steps: int = 5) -> str:
    for s in range(max_steps):
        p = str(V_DIR / f"shot_{time.strftime('%Y%m%d_%H%M%S')}.png")
        try: pyautogui.screenshot(p)
        except: return "ERROR: Screenshot failed"
        try:
            r = json.loads(re.sub(r'```(?:json)?\s*|\s*```', '', llm_call(f"Screenshot: {p}\nTask: {cmd}\nStep {s+1}/{max_steps}\nNUR valide JSON: {{\"description\": \"...\", \"action\": \"click|type|scroll|move|done\", \"params\": ...}}", "Vision-Loop-Agent"), flags=re.DOTALL))
            if not _val(r) or r.get("action") == "done": auto_commit(".", "Vision Loop Done"); return f"✅ Vision-Loop fertig: {r.get('description', 'Erledigt')}"
            a, p_ = r.get("action"), r.get("params", "")
            if a == "click": pyautogui.click()
            elif a == "type": pyautogui.typewrite(str(p_))
            elif a == "scroll": pyautogui.scroll(int(p_ if str(p_).isdigit() or (str(p_)[0]=='-' and str(p_)[1:].isdigit()) else 500))
            evaluate_job(cmd, f"Step {s}: {r.get('description','')}"); auto_commit(".", f"Vision Step {s}")
        except Exception as e: safe_run_command(f"echo 'Vision Error Step {s}: {str(e)}' >> .backups/sandbox.log", "visionAG")
    return "⏹️ Vision-Loop pausiert (Max-Schritte)"
