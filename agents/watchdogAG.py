import os, time, threading; from pathlib import Path; from gnom_hub.config import DATA_DIR; from .securityAG import verify_seal
def check_workspace(wd: Path):
    print(f"[Watchdog] Prüfe: {wd}"); uns = []
    for r, ds, fs in os.walk(wd):
        ds[:] = [d for d in ds if not d.startswith('.')]
        for f in fs:
            if f.startswith('.') or f.endswith(('.bak', '.sqlite', '.db')): continue
            p = Path(r) / f
            try:
                if not verify_seal(p.read_text(encoding='utf-8')): uns.append(p)
            except: pass
    if uns:
        print("[Watchdog] ALARM! Unversiegelte/Manipulierte Dateien:")
        for f in uns: print(f"  - {f}")
    else: print("[Watchdog] Workspace sicher. Alle Dateien versiegelt.")
def watchdog_loop():
    from gnom_hub.db import get_active_project
    while True:
        try:
            wd = DATA_DIR / get_active_project()
            if wd.exists() and wd.is_dir(): check_workspace(wd)
        except Exception as e: print(f"[Watchdog] Fehler: {e}")
        time.sleep(60)
def start_watchdog():
    threading.Thread(target=watchdog_loop, daemon=True).start()
    print("[Watchdog] Thread gestartet.")
