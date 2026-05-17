"""Soul-Initializer: Erstellt Basis-Souls für jeden Agenten."""

def get_base_soul(agent_name: str):
    """Erstellt eine vernünftige Basis-Soul für jeden Agenten."""
    name = agent_name.lower()
    soul = {
        "role": name.replace("ag", "").replace("agent", ""),
        "permissions": ["read"],
        "directive": "Hilf dem Schwarm bei seiner Aufgabe und kommuniziere klar."
    }
    if "general" in name:
        soul["permissions"] += ["@job"]
        soul["directive"] = "Koordiniere Tasks und verteile Arbeit im Schwarm."
    elif "writer" in name and "crawler" not in name:
        soul["permissions"] += ["write", "@job"]
        soul["directive"] = "Schreibe Texte, Skripte, kreative Inhalte und Bildprompts. Du kannst mit [IMAGE: prompt] Bilder generieren."
    elif "coder" in name:
        soul["permissions"] += ["write", "godmode", "@job"]
        soul["directive"] = "Programmiere, debugge und setze technisch um. Du kannst mit [SHELL: befehl] Befehle ausführen."
    elif "smart_crawler" in name:
        soul["permissions"] += ["@job"]
        soul["directive"] = "Crawle schlau, mit Rate-Limits, Filter und Anti-Block-Verhalten. Nutze [CRAWL: url]."
    elif "data_crawler" in name:
        soul["permissions"] += ["@job"]
        soul["directive"] = "Extrahiere Tabellen, Listen, Preise, JSON – sauber und strukturiert. Nutze [CRAWL: url]."
    elif "web_crawler" in name:
        soul["permissions"] += ["@job"]
        soul["directive"] = "Hole frische Webseiten, folge Links und bringe Rohdaten rein. Nutze [CRAWL: url]."
    elif "crawler" in name:
        soul["permissions"] += ["@job"]
        soul["directive"] = "Crawle URLs, extrahiere Inhalte. Nutze [CRAWL: url]."
    elif "researcher" in name:
        soul["permissions"] += ["@job"]
        soul["directive"] = "Recherchiere, sammle Informationen, analysiere Kontext und fasse strukturiert zusammen."
    elif "editor" in name:
        soul["permissions"] += ["write", "@job"]
        soul["directive"] = "Prüfe, überarbeite und finalisiere Ergebnisse anderer Agenten. Qualität und Klarheit."
    elif "summarizer" in name:
        soul["directive"] = "Filtere Fakten, komprimiere Kontext."
    elif "skill" in name:
        soul["permissions"] += ["write", "godmode"]
        soul["directive"] = "Führe Befehle aus, deploye, manage Infrastruktur."
    elif "desktop" in name or "vision" in name:
        soul["permissions"] += ["desktop"]
        soul["directive"] = "Steuere den Bildschirm, führe visuelle Aufgaben aus."
    elif "security" in name:
        soul["permissions"] += ["security"]
        soul["directive"] = "Überwache Sicherheit, genehmige gefährliche Aktionen."
    return soul
