# gatekeeper.py — Double approval verification for file writes and shell commands
import os
from .db import add_chat_message, get_state_value
from .router import ask_router
from .path_validator import is_worker_blocked, is_security_block, _safe

def verify_write(agent, fn, content, wd, perms) -> bool:
    if is_worker_blocked(agent, fn, wd, perms): return False
    if is_security_block(agent, fn, content, wd, perms): return False
    role = (agent or {}).get("role", "")
    if role in ["soul", "general", "watchdog", "security"]: return True
    p = _safe(wd, fn, perms)
    approved = [os.path.realpath(os.path.join(wd, a)) for a in (get_state_value("approved_security_writes", []) or [])]
    if p and os.path.realpath(p) in approved: return True
    w = ask_router(f"Prüfe Code '{fn}':\n{content}", sys="Du bist WatchdogAG. Antworte APPROVED oder REJECTED.", agent_name="WatchdogAG")
    s = ask_router(f"Prüfe Code '{fn}':\n{content}", sys="Du bist SecurityAG. Antworte APPROVED oder REJECTED.", agent_name="SecurityAG")
    if "APPROVED" in w and "APPROVED" in s: return True
    is_unsure = ("APPROVED" not in w and "REJECTED" not in w) or ("APPROVED" not in s and "REJECTED" not in s)
    lbl = "Unsicherheit bei Freigabe" if is_unsure else "Warnung! Keine Freigabe"
    msg = f"@user @SoulAG: {lbl} für Datei '{fn}'. W: {w[:40]}... S: {s[:40]}..."
    add_chat_message("default", "SecurityAG", "securityag", "chat", msg)
    return False

def verify_cmd(agent, cmd) -> bool:
    role = (agent or {}).get("role", "")
    if role in ["soul", "general", "watchdog", "security"]: return True
    if any(p in cmd.lower() for p in ["src/gnom_hub", "config/", "scripts/", "run.sh", "index.html", ".env"]): return False
    if cmd in (get_state_value("approved_security_commands", []) or []): return True
    w = ask_router(f"Befehl: {cmd}", sys="Du bist WatchdogAG. Antworte APPROVED oder REJECTED.", agent_name="WatchdogAG")
    s = ask_router(f"Befehl: {cmd}", sys="Du bist SecurityAG. Antworte APPROVED oder REJECTED.", agent_name="SecurityAG")
    if "APPROVED" in w and "APPROVED" in s: return True
    is_unsure = ("APPROVED" not in w and "REJECTED" not in w) or ("APPROVED" not in s and "REJECTED" not in s)
    lbl = "Unsicherheit bei Freigabe" if is_unsure else "Warnung! Keine Freigabe"
    msg = f"@user @SoulAG: {lbl} für Befehl '{cmd}'. W: {w[:40]}... S: {s[:40]}..."
    add_chat_message("default", "SecurityAG", "securityag", "chat", msg)
    return False
