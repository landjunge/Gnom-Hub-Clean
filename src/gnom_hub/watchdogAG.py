import os
import time
from pathlib import Path
import threading
from .config import DATA_DIR
from .securityAG import verify_seal

WATCHDOG_INTERVAL = 60  # seconds

def check_workspace(workspace_dir: Path):
    """Prüft alle Dateien im Workspace auf gültige ZWC-Siegel."""
    print(f"[Watchdog] Prüfe Workspace: {workspace_dir}")
    unsealed_files = []
    
    for root, dirs, files in os.walk(workspace_dir):
        # Überspringe .git und andere versteckte Ordner
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            # Überspringe versteckte Dateien oder bestimmte Endungen
            if file.startswith('.') or file.endswith(('.bak', '.sqlite', '.db')):
                continue
                
            file_path = Path(root) / file
            try:
                content = file_path.read_text(encoding='utf-8')
                if not verify_seal(content):
                    unsealed_files.append(file_path)
            except Exception as e:
                # Ignoriere binäre Dateien oder Lese-Fehler
                pass
                
    if unsealed_files:
        print("[Watchdog] ALARM! Unversiegelte oder manipulierte Dateien gefunden:")
        for f in unsealed_files:
            print(f"  - {f}")
        # Hier könnte man die Dateien in Quarantäne verschieben oder löschen
        # Für den Anfang loggen wir es nur.
    else:
        print("[Watchdog] Workspace ist sicher. Alle Dateien sind korrekt versiegelt.")

def watchdog_loop():
    """Hintergrund-Loop für den Watchdog."""
    from .db import get_active_project
    while True:
        try:
            # Wir prüfen das aktuelle Projekt-Verzeichnis
            active_proj = get_active_project()
            workspace_dir = DATA_DIR / active_proj
            if workspace_dir.exists() and workspace_dir.is_dir():
                check_workspace(workspace_dir)
        except Exception as e:
            print(f"[Watchdog] Fehler im Loop: {e}")
        time.sleep(WATCHDOG_INTERVAL)

def start_watchdog():
    """Startet den Watchdog in einem eigenen Thread."""
    t = threading.Thread(target=watchdog_loop, daemon=True)
    t.start()
    print("[Watchdog] Wächter-Thread gestartet.")
