# action_write.py — Verarbeitet [WRITE:] und [READ:] Tags
import os

def handle_write(answer, matches, agent, perms, bs_mode, wd):
    from .securityAG import seal_content
    for m in matches:
        fname, content = m.group(1).strip(), m.group(2).strip()
        if bs_mode:
            answer = answer.replace(m.group(0), f"[System: WRITE blockiert im Brainstorm-Modus. Nutze @{agent['name']} für Einzelauftrag.]")
        elif "write" not in perms:
            answer = answer.replace(m.group(0), f"[System: {agent['name']} hat keine WRITE-Berechtigung.]")
        else:
            try:
                fpath = os.path.join(wd, fname)
                if os.path.exists(fpath):
                    import shutil; shutil.copy2(fpath, fpath + ".bak")
                sealed_content = seal_content(agent["name"], content)
                with open(fpath, "w") as f: f.write(sealed_content)
                answer = answer.replace(m.group(0), f"[System: Datei '{fname}' wurde erfolgreich im Workspace gespeichert.]")
            except Exception as e:
                answer = answer.replace(m.group(0), f"[System-Fehler beim Speichern von {fname}: {e}]")
    return answer

def handle_read(answer, matches, wd):
    for m in matches:
        fname = m.group(1).strip()
        p = os.path.join(wd, fname)
        if os.path.exists(p):
            c = open(p, "r").read()[:2000]
            answer = answer.replace(m.group(0), f"[Hat {fname} gelesen:\n{c}\n...]")
        else:
            answer = answer.replace(m.group(0), f"[Fehler: Datei {fname} nicht gefunden]")
    return answer
