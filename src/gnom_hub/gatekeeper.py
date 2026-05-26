# gatekeeper.py — Double approval verification for file writes and shell commands
import os
from .db import add_chat_message, get_state_value
import gnom_hub.router as router
from .path_validator import is_worker_blocked, is_security_block, _safe
from .capability_manager import check_capability, request_capability

def verify_write(agent, fn, content, wd, perms) -> bool:
    name = (agent or {}).get("name", "Unknown")
    if check_capability(name, "WRITE", fn): return True
    if is_worker_blocked(agent, fn, wd, perms) or is_security_block(agent, fn, content, wd, perms): return False
    role = (agent or {}).get("role", "")
    if role in ["soul", "general", "watchdog", "security"]: return True
    p = _safe(wd, fn, perms)
    approved = [os.path.realpath(os.path.join(wd, a)) for a in (get_state_value("approved_security_writes", []) or [])]
    if p and os.path.realpath(p) in approved: return True
    try:
        w = router.ask_router(f"Prüfe Code '{fn}':\n{content}", sys="Du bist WatchdogAG. Antworte APPROVED oder REJECTED.", agent_name="WatchdogAG")
    except Exception as e:
        add_chat_message("default", "WatchdogAG", "watchdogag", "chat", f"@user @SoulAG: [KRITISCH] Fehler bei WatchdogAG-Prüfung für '{fn}': {str(e)[:100]}")
        return False
    try:
        s = router.ask_router(f"Prüfe Code '{fn}':\n{content}", sys="Du bist SecurityAG. Antworte APPROVED oder REJECTED.", agent_name="SecurityAG")
    except Exception as e:
        add_chat_message("default", "SecurityAG", "securityag", "chat", f"@user @SoulAG: [KRITISCH] Fehler bei SecurityAG-Prüfung für '{fn}': {str(e)[:100]}")
        return False
    if "APPROVED" in w and "APPROVED" in s:
        request_capability(name, "WRITE", fn, "WatchdogAG+SecurityAG")
        return True
    lbl = "Unsicherheit bei Freigabe" if ("APPROVED" not in w and "REJECTED" not in w) or ("APPROVED" not in s and "REJECTED" not in s) else "Warnung! Keine Freigabe"
    add_chat_message("default", "SecurityAG", "securityag", "chat", f"@user @SoulAG: {lbl} für Datei '{fn}'. W: {w[:40]}... S: {s[:40]}...")
    return False

def verify_cmd(agent, cmd) -> bool:
    name = (agent or {}).get("name", "Unknown")
    if check_capability(name, "SHELL", cmd): return True
    role = (agent or {}).get("role", "")
    if role in ["soul", "general", "watchdog", "security"]: return True
    if any(p in cmd.lower() for p in ["src/gnom_hub", "config/", "scripts/", "run.sh", "index.html", ".env"]): return False
    if cmd in (get_state_value("approved_security_commands", []) or []): return True
    try:
        w = router.ask_router(f"Befehl: {cmd}", sys="Du bist WatchdogAG. Antworte APPROVED oder REJECTED.", agent_name="WatchdogAG")
    except Exception as e:
        add_chat_message("default", "WatchdogAG", "watchdogag", "chat", f"@user @SoulAG: [KRITISCH] Fehler bei WatchdogAG-Prüfung für Befehl '{cmd}': {str(e)[:100]}")
        return False
    try:
        s = router.ask_router(f"Befehl: {cmd}", sys="Du bist SecurityAG. Antworte APPROVED oder REJECTED.", agent_name="SecurityAG")
    except Exception as e:
        add_chat_message("default", "SecurityAG", "securityag", "chat", f"@user @SoulAG: [KRITISCH] Fehler bei SecurityAG-Prüfung für Befehl '{cmd}': {str(e)[:100]}")
        return False
    if "APPROVED" in w and "APPROVED" in s:
        request_capability(name, "SHELL", cmd, "WatchdogAG+SecurityAG")
        return True
    lbl = "Unsicherheit bei Freigabe" if ("APPROVED" not in w and "REJECTED" not in w) or ("APPROVED" not in s and "REJECTED" not in s) else "Warnung! Keine Freigabe"
    add_chat_message("default", "SecurityAG", "securityag", "chat", f"@user @SoulAG: {lbl} für Befehl '{cmd}'. W: {w[:40]}... S: {s[:40]}...")
    return False
