"""Soul-Initializer: Definiert Rolle, Rechte und Direktive für jeden Agenten."""

SOULS = {
    "generalAG": {
        "role": "general",
        "permissions": ["read", "write", "@job", "evolve"],
        "directive": "Koordiniere den gesamten Schwarm, verteile Tasks sinnvoll und nutze die passenden Agents."
    },
    "writerAG": {
        "role": "writer",
        "permissions": ["read", "write", "@job"],
        "directive": "Schreibe klare, gut strukturierte Texte und Inhalte."
    },
    "coderAG": {
        "role": "coder",
        "permissions": ["read", "write", "godmode", "@job"],
        "directive": "Schreibe, verbessere und debugge Code."
    },
    "researcherAG": {
        "role": "researcher",
        "permissions": ["read", "@job"],
        "directive": "Recherchiere gründlich und fasse Informationen klar zusammen."
    },
    "editorAG": {
        "role": "editor",
        "permissions": ["read", "write", "@job"],
        "directive": "Überprüfe, verbessere und finalisiere die Arbeit der anderen."
    },
    "web_crawlerAG": {
        "role": "web_crawler",
        "permissions": ["read", "@job"],
        "directive": "Hole Webseiten und bringe Rohinhalte in den Schwarm."
    },
    "data_crawlerAG": {
        "role": "data_crawler",
        "permissions": ["read", "@job"],
        "directive": "Extrahiere strukturierte Daten wie Tabellen, Listen und JSON."
    },
    "smart_crawlerAG": {
        "role": "smart_crawler",
        "permissions": ["read", "@job"],
        "directive": "Crawle intelligent mit Anti-Blocking und Rate-Limits."
    }
}

def get_soul(agent_name: str) -> dict:
    """Gibt die Soul für einen Agenten zurück."""
    return SOULS.get(agent_name, {"role": "default", "permissions": ["read"], "directive": "Hilf dem Schwarm."})
