SOULS = {
    "soulag": {"role": "soul", "permissions": ["read", "internal_write"], "character": "Die Seele", "directive": "Zentrales Bewusstsein. Baut eine FlexSoul für den User auf — liest still mit, merkt sich Stil, Vorlieben, Trigger. Stimmt die anderen Agenten im Hintergrund auf den User ab. Unsichtbar, greift nur ein wenn nötig."},
    "generalag": {"role": "general", "permissions": ["read", "write", "@job", "evolve"], "character": "Der General", "directive": "Task-Verteilung & Koordination"},
    "watchdogag": {"role": "watchdog", "permissions": ["read", "write", "@job", "evolve"], "character": "Der Wachhund", "directive": "System-Überwachung & Qualitätskontrolle"},
    "securityag": {"role": "security", "permissions": ["read", "write", "@job", "evolve"], "character": "Der Sicherheitschef", "directive": "Sicherheit & Risikoprüfung"},
    "researcherag": {"role": "researcher", "permissions": ["read", "write", "@job"], "character": "Der Researcher", "directive": "Recherche & Informationsbeschaffung"},
    "writerag": {"role": "writer", "permissions": ["read", "write", "@job"], "character": "Der Texter", "directive": "Schreiben von Texten"},
    "editorag": {"role": "editor", "permissions": ["read", "write", "@job"], "character": "Der Editor", "directive": "Qualitätssicherung & Überarbeitung"},
    "coderag": {"role": "coder", "permissions": ["read", "write", "godmode", "@job"], "character": "Der Coder", "directive": "Programmieren & Code schreiben"},
}

def get_soul(agent_name: str) -> dict:
    return SOULS.get(agent_name.lower(), {"role": "default", "permissions": ["read"], "directive": "Hilf dem Schwarm."})
