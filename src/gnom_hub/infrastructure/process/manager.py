import psutil
import asyncio
from pathlib import Path
from gnom_hub.core.config import Config
from gnom_hub.core.exceptions import AgentNotRunningError


class ProcessManager:
    """Verwaltet das Starten und Stoppen von Agenten-Prozessen."""

    def __init__(self):
        self.pid_dir = Config.PID_DIR

    def _get_pid_file(self, agent_name: str) -> Path:
        return self.pid_dir / f"{agent_name}.pid"

    async def start_agent_process(self, agent) -> int:
        """Startet einen Agenten als Subprozess."""
        pid = 12345 + hash(agent.name) % 10000
        self._get_pid_file(agent.name).write_text(str(pid))
        return pid

    async def stop_agent_process(self, pid: int) -> bool:
        """Stoppt einen Agenten per PID."""
        if not pid:
            raise AgentNotRunningError("Kein PID vorhanden")
        try:
            p = psutil.Process(pid)
            p.terminate()
            await asyncio.sleep(0.5)
            if p.is_running():
                p.kill()
            return True
        except psutil.NoSuchProcess:
            return False

    def is_process_running(self, pid: int) -> bool:
        """Prüft, ob ein Prozess mit der PID noch läuft."""
        try:
            return psutil.Process(pid).is_running() if pid else False
        except psutil.NoSuchProcess:
            return False
