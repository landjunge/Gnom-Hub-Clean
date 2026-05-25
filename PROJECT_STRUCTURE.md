# 🧠 Gnom-Hub – Projektstruktur & Architektur

Dieses Dokument beschreibt die finale Ordnerstruktur und Architektur von **Gnom-Hub**. Das Projekt folgt den Prinzipien der **Clean Architecture**, sodass die Abhängigkeiten strikt von außen nach innen verlaufen.

---

### Abhängigkeitsregel (The Dependency Rule)

**Äußere Schichten dürfen innere Schichten kennen – umgekehrt nie.**

Die `domain` ist das Herzstück des Systems und enthält keinerlei technische Abhängigkeiten.

---

### Ordnerstruktur

```text
src/gnom_hub/
├── core/                    # Globale Konfiguration & Utilities
│   ├── config.py
│   └── logger.py
│
├── common/                  # Schichtenübergreifende Komponenten
│   └── exceptions.py
│
├── domain/                  # Geschäftsregeln & Datenmodelle
│   ├── agent/
│   │   ├── entities.py
│   │   └── repository.py
│   ├── chat/
│   │   ├── entities.py
│   │   └── repository.py
│   └── workspace/
│       ├── entities.py
│       └── rules.py
│
├── application/             # Anwendungsfälle (Use Cases)
│   ├── agent/
│   │   ├── commands.py
│   │   └── queries.py
│   ├── chat/
│   │   ├── send_message.py
│   │   ├── brainstorm.py
│   │   └── service.py
│   ├── security/
│   │   ├── verify_files.py
│   │   └── policy.py
│   └── workspace/
│       └── validation.py
│
├── infrastructure/          # Technische Implementierungen
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.py
│   │   ├── agent_repo.py
│   │   └── chat_repo.py
│   ├── process/
│   │   └── manager.py
│   └── llm/
│       ├── openrouter.py
│       ├── ollama.py
│       └── orchestrator.py
│
├── presentation/            # API-Schicht
│   ├── api/
│   │   ├── v1/
│   │   │   ├── agents.py
│   │   │   ├── chat.py
│   │   │   └── admin.py
│   │   └── router.py
│   └── app.py
│
└── __main__.py
```

---

### Schicht-Beschreibungen

- **`domain/`** – Reine Geschäftslogik und Entitäten. Keine Abhängigkeiten zu externen Frameworks oder Datenbanken.
- **`application/`** – Use Cases, Orchestrierung und Anwendungslogik. Koordiniert den Fluss zwischen Domain und Infrastructure.
- **`infrastructure/`** – Konkrete Implementierungen (Datenbank, LLM-Clients, Prozessmanagement).
- **`presentation/`** – FastAPI-Router und Web-Schnittstelle.
- **`common/`** – Systemweit genutzte Exceptions und Utilities.
- **`core/`** – Konfiguration, Logging und globale Hilfsmittel.
