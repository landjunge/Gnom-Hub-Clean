import subprocess, signal, os, sys
def find_process(name):
    try:
        if str(name).isdigit():
            out = subprocess.check_output(f"lsof -ti:{name}", shell=True).decode().strip()
        else:
            out = subprocess.check_output(["pgrep", "-if", name]).decode().strip()
        return [int(p) for p in out.split("\n") if p]
    except: return []
def kill_process(target):
    pids = find_process(target)
    for pid in pids:
        if pid != os.getpid():
            try: os.kill(pid, signal.SIGTERM)
            except: pass
    return f"Killed {target}: {pids}"
def restart_hub(): os._exit(42)
def start_background_agents():
    os.makedirs("logs", exist_ok=True)
    for a in ["generalAG", "soulAG", "researcherAG", "writerAG", "editorAG", "coderAG"]:
        kill_process(a)
        f = open(f"logs/logs_{a.lower()[:-2]}.txt", "w")
        subprocess.Popen([sys.executable, "-u", "-m", f"agents.{a}"], stdout=f, stderr=subprocess.STDOUT)
def kill_background_agents():
    for a in ["generalAG", "soulAG", "researcherAG", "writerAG", "editorAG", "coderAG"]:
        kill_process(a)
def process_status():
    try:
        out = subprocess.check_output("ps aux | grep -E 'gnom.hub|watchdog|general|soul|researcher|writer|editor|coder' | grep -v grep", shell=True).decode()
        return out.strip() or "No gnom-hub processes found"
    except: return "No gnom-hub processes found"

