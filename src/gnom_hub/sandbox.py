# sandbox.py — Hybrid Docker & macOS Sandbox Executor
import subprocess, os
from .config import WORKSPACE_DIR
from .sandbox_exec import run_sandboxed

def is_docker_running():
    try:
        return subprocess.run(["docker", "ps"], capture_output=True, timeout=2).returncode == 0
    except:
        return False

def run_in_sandbox(command: str, timeout: int = 30):
    wd = os.path.abspath(str(WORKSPACE_DIR))
    if is_docker_running():
        cmd = [
            "docker", "run", "--rm", "--network=none", "--memory=512m", "--cpus=1",
            "-w", "/workspace", "-v", f"{wd}:/workspace:rw", "python:3.11-slim", "bash", "-c", command
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return subprocess.CompletedProcess(args=cmd, returncode=r.returncode, stdout=r.stdout, stderr=r.stderr)
        except Exception:
            pass
    return run_sandboxed(command, wd, timeout=timeout)
