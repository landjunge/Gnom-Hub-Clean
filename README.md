# GnomHub - Clean Architecture Edition

Saubere, modulare Multi-Agenten-Plattform nach Clean Architecture Prinzipien.

## ✨ Features
- Strenge Clean Architecture mit klarer Trennung der Schichten
- Jede Datei maximal 40 Zeilen (40-Line Rule)
- Vollständige Dependency Injection
- Agenten-Management (Starten, Stoppen, Registrieren)
- Chat-System mit Langzeitgedächtnis (FlexSoul)
- Paralleles Brainstorming mit mehreren Agenten
- Ollama-Support (lokal) + OpenRouter Fallback
- SQLite Datenbank mit WAL-Modus

## 🚀 Schnellstart

```bash
chmod +x run.sh
./run.sh
```

## 🗺️ Wichtige API-Endpunkte
- **GET** `/agents/` — Alle Agenten anzeigen
- **POST** `/agents/register?name=Demo&model=llama3` — Neuen Agenten registrieren
- **POST** `/chat/send?agent_id=...&content=Deine Nachricht` — Mit einem Agenten chatten
- **POST** `/admin/nuke` — Datenbank komplett zurücksetzen

## 🛠️ Technologie-Stack
- Python 3 · FastAPI · SQLite · Ollama · Clean Architecture

---
**Version:** Clean Architecture Refactoring (Mai 2026)  
Dies ist die saubere, neu strukturierte Version des GnomHub.