"""Prozess-Management für Gnom-Hub Watchdog."""
import subprocess, signal, os
def find_process(name_or_port):
    """Findet PID nach Name oder Port."""
    try:
        if str(name_or_port).isdigit():
            out = subprocess.check_output(f"lsof -ti:{name_or_port}", shell=True).decode().strip()
            return [int(p) for p in out.split("\n") if p]
        out = subprocess.check_output(["pgrep", "-f", name_or_port]).decode().strip()
        return [int(p) for p in out.split("\n") if p]
    except: return []
def kill_process(target):
    """Killt Prozess nach Name oder Port."""
    pids = find_process(target)
    for pid in pids:
        if pid == os.getpid(): continue
        try: os.kill(pid, signal.SIGTERM)
        except: pass
    return f"Killed processes: {pids}"
def restart_hub():
    """Startet Gnom-Hub neu durch sauberen Exit mit Code 42."""
    import os
    os._exit(42)
    return "Hub restart initiated"
def process_status():
    """Zeigt laufende Gnom-Hub Prozesse."""
    try:
        out = subprocess.check_output("ps aux | grep -E 'gnom.hub|tiny_agent|watchdog|general|summarizer|soul|cronjob|apikeys|skills' | grep -v grep", shell=True).decode()
        return out.strip() or "No gnom-hub processes found"
    except: return "No gnom-hub processes found"
