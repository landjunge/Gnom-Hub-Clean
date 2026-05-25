# 🧠 GNOM-HUB — Multi-Agenten-Plattform

Eine leichtgewichtige, modulare Multi-Agenten-Plattform basierend auf robusten Clean-Architecture-Prinzipien und einer radikalen Restriktion: **Jedes Backend-Modul ist auf maximal 40 Zeilen Python-Code begrenzt** (die 40-Zeilen-Regel). Die Steuerung des Agenten-Schwarms erfolgt über ein modernes Web-Dashboard namens **War Room**.

---

## 🤖 Die 8 Agenten
Gnom-Hub orchestriert einen Schwarm von 8 Agenten, aufgeteilt in 4 koordinierende System-Agenten und 4 spezialisierte Worker-Agenten:

### System-Agenten (Volle Werkzeug-Rechte)
System-Agenten verwalten die Infrastruktur und besitzen umfassende Berechtigungen (`read`, `write`, `run`, `godmode`, `crawl`, `desktop`, `evolve`):
* **SoulAG**: Das zentrale Gedächtnis des Schwarms. Lernt den Stil und die Vorlieben des Nutzers im Hintergrund und injiziert diese kontextbezogen in die Prompts.
* **GeneralAG**: Der Hauptkoordinator. Analysiert komplexe Aufgaben, warnt vor Regelverstößen (z. B. Dateilängen) und delegiert präzise Teilaufgaben an die Worker.
* **WatchdogAG**: Überwacht zyklisch die Integrität des Workspace und die Einhaltung der Systemgrenzen.
* **SecurityAG**: Führt Risikoprüfungen und Sicherheitsüberwachungen durch.

### Worker-Agenten (Eingeschränkte Werkzeug-Rechte)
Worker-Agenten erledigen die eigentliche Arbeit im Workspace. Sie besitzen standardmäßig nur Workspace-Schreibrechte (`read`, `write`, `@job`):
* **CoderAG**: Implementiert, debuggt und führt Code aus (erhält durch `godmode` zusätzlich Terminal- und Browserrechte).
* **ResearcherAG**: Führt Recherchen durch, fragt Such-APIs ab und validiert Quellen.
* **WriterAG**: Entwirft Dokumentationen, Tutorials, Berichte und kreative Texte.
* **EditorAG**: Führt Korrekturlesen, Stilprüfungen und Qualitätskontrollen durch.

---

## 🎛️ Das Preset-System (6 Modi)
Das Preset-System erlaubt es, den Fokus und die Modelle der Worker-Agenten mit einem Klick anzupassen. Das Dropdown-Menü befindet sich in der linken Seitenleiste direkt unter der Showbox:

1. 💻 **Web Development**: Fokus auf sauberen HTML, CSS, JavaScript-Code, Responsive Layouts, Barrierefreiheit (ARIA) und Web-APIs.
2. 🎨 **Graphic Design**: Fokus auf visuelle Ästhetik, Typografie, Farbharmonien, Grids und inline SVG-Generierung.
3. 🎵 **Audio Production**: Fokus auf Web Audio API, Sound-Synthese, DSP-Programmierung und Sounddesign.
4. 🎬 **Video Production**: Fokus auf Canvas-Animationen, requestAnimationFrame-Schleifen und Videokonzepte.
5. ✍️ **Marketing & Copy**: Fokus auf überzeugende Werbetexte, SEO-Optimierung und Conversion-Hooks (AIDA-Formel).
6. 🔍 **Research & Analysis**: Fokus auf tiefgehende Recherche, Datenanalyse (Python-Skripte), Faktenprüfung und strukturierte Berichte.

### Funktionsweise
* **Auswahl & Feedback**: Der Nutzer wählt das Preset über das Dropdown-Menü aus. Die Showbox zeigt sofort den Schwerpunkt an, und im Chat erscheint eine Bestätigung vom System.
* **Modell- & Prompt-Anpassung**: Der Preset-Service und der LLM-Router passen die 4 Worker-Agenten (`CoderAG`, `ResearcherAG`, `WriterAG`, `EditorAG`) automatisch an:
  * **Modelle**: Optimale Standardmodelle werden geladen (z. B. spezialisierte Coder-Modelle für Web Dev).
  * **System-Prompts**: Modifikatoren werden dynamisch in die LLM-Anfragen injiziert, um den Arbeitsstil anzupassen.
* **Benutzerdefinierte Einstellungen**: Speichert der Nutzer eigene Modelle für die Worker in den Einstellungen, werden diese an das aktive Preset gebunden und beim nächsten Wechsel automatisch wiederhergestellt.

---

## 🚀 Schnellstart
Stellen Sie sicher, dass Ihre API-Keys (z. B. OpenRouter oder DeepSeek) in `config/.env` eingetragen sind.

1. **Server und Agenten starten**:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
2. **Dashboard öffnen**:
   Navigieren Sie im Browser zu: **[http://127.0.0.1:3002](http://127.0.0.1:3002)**

---

## 🔌 Wichtige API-Endpunkte
Gnom-Hub bietet eine REST-API zur vollständigen Steuerung des Schwarms:

* **Presets**:
  * `GET /api/admin/preset` — Gibt das aktive Preset zurück.
  * `POST /api/admin/preset` — Wechselt das aktive Preset. Body: `{"preset": "Name"}`
* **Agenten**:
  * `GET /api/agents` — Listet alle registrierten Agenten, deren PIDs und Status auf.
  * `POST /api/agents/register` — Registriert oder aktualisiert einen Agenten im System.
  * `POST /api/agents/{agent_id}/start` / `stop` — Startet oder stoppt Agentenprozesse.
* **Chat**:
  * `GET /api/chat?limit=50` — Ruft den Chatverlauf ab (mit bereinigten Showbox-Signaturen).
  * `POST /api/chat` — Postet eine neue Nachricht.
* **LLM-Verwaltung**:
  * `POST /api/llm/agents` — Speichert benutzerdefinierte Modellzuweisungen für das aktive Preset.

---

## 🛠️ Technologie-Stack
* **Core-Backend**: FastAPI & Uvicorn (Asynchroner Python-Webserver).
* **Datenhaltung**: SQLite3 (WAL-Modus für lock-freie, transaktionssichere Schreibzugriffe).
* **Prozess-Manager**: `psutil` (plattformunabhängiges Management der Agentenprozesse über PID-Dateien).
* **Frontend**: HTML5, Vanilla CSS3 (Custom-Properties, HSL-Farben, Glassmorphismus, responsive Layouts), pure JavaScript (Fetch-API, Event-Handling).
* **LLM-Integration**: Lokale Ollama-Instanzen & Cloud-Anbindung an OpenRouter / DeepSeek.