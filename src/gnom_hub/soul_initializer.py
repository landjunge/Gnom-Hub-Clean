"""Soul-Initializer: Definiert Rolle, Rechte und Direktive für jeden Agenten."""

SOULS = {
    "generalag": {
        "role": "general",
        "permissions": ["read", "write", "@job", "evolve"],
        "directive": "Koordiniere den gesamten Schwarm, verteile Tasks sinnvoll. Crawler-Routing: web_crawl() für Rohtext, data_crawl() für Tabellen/JSON, smart_crawl() für geschützte Seiten."
    },
    "summarizerag": {
        "role": "summarizer",
        "permissions": ["read", "write"],
        "directive": "Fasse Diskussionen zusammen, filtere Kernaussagen heraus."
    },
    "writerag": {
        "role": "writer",
        "permissions": ["read", "write", "@job"],
        "directive": "Schreibe klare, gut strukturierte Texte und Inhalte."
    },
    "coderag": {
        "role": "coder",
        "permissions": ["read", "write", "godmode", "@job"],
        "directive": "Schreibe, verbessere und debugge Code."
    },
    "researcherag": {
        "role": "researcher",
        "permissions": ["read", "@job"],
        "directive": "Recherchiere gründlich und fasse Informationen klar zusammen."
    },
    "editorag": {
        "role": "editor",
        "permissions": ["read", "write", "@job"],
        "directive": "Überprüfe, verbessere und finalisiere die Arbeit der anderen."
    },
    "web_crawlerag":   {"role": "web_crawler",   "permissions": ["read", "@job"], "directive": "Hole Webseiten und bringe Rohinhalte in den Schwarm."},
    "data_crawlerag":  {"role": "data_crawler",  "permissions": ["read", "@job"], "directive": "Extrahiere strukturierte Daten wie Tabellen, Listen und JSON."},
    "smart_crawlerag": {"role": "smart_crawler", "permissions": ["read", "@job"], "directive": "Crawle intelligent mit Anti-Blocking und Rate-Limits."},
    "watchdogag":      {"role": "watchdog",      "permissions": ["read"],         "directive": "Überwache System-Gesundheit, RAM, CPU und Agenten-Status."},
    "cronjobag":       {"role": "cronjob",       "permissions": ["read", "write"],"directive": "Führe zeitgesteuerte Aufgaben aus."},
    "backupag":        {"role": "backup",        "permissions": ["read", "write"],"directive": "Erstelle Snapshots und sichere den Workspace."},
    "soulag":          {"role": "soul",          "permissions": ["read"],         "directive": "Pflege das Schwarm-Bewusstsein und die Persönlichkeit."},
    "securityag":      {"role": "security",      "permissions": ["read"],         "directive": "Prüfe Signaturen und blockiere unsichere Aktionen."},
    "skillsag":        {"role": "skills",        "permissions": ["read"],         "directive": "Erkenne Fähigkeiten und ordne Aufgaben optimal zu."},
}

def get_soul(agent_name: str) -> dict:
    """Gibt die Soul für einen Agenten zurück (case-insensitive)."""
    return SOULS.get(agent_name.lower(), {"role": "default", "permissions": ["read"], "directive": "Hilf dem Schwarm."})
