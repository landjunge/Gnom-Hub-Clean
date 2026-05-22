# 🧠 GNOM-HUB

> **Ein leichtgewichtiges, selbstheilendes Multi-Agenten-Orchestrierungssystem für Entwickler.**

[![Language](https://img.shields.io/badge/Sprache-Deutsch-blue.svg)](#)
[![License](https://img.shields.io/badge/Lizenz-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](#)

*Read this in [English](README_EN.md)*

---

**Gnom-Hub** ist eine extrem schlanke, lokale Multi-Agenten-Umgebung, die für maximale Effizienz und Transparenz entwickelt wurde. Im Gegensatz zu überladenen Frameworks setzt Gnom-Hub auf radikalen Minimalismus: **Jedes Modul und jeder Agent umfasst maximal 40 Zeilen logischen Code.** 

Trotz dieser minimalen Codebasis verfügt das System über fortgeschrittene Fähigkeiten: Agenten können via PyAutoGUI und Playwright deinen Bildschirm wahrnehmen, Maus und Tastatur steuern, ihren eigenen Code bei Fehlern autonom umschreiben (Selbst-Evolution) und sämtliche Aktionen revisionssicher über ein automatisches Git-Versionierungssystem dokumentieren. Orchestriert wird dieser Agentenschwarm in einem cyberpunke-esken Web-Dashboard – dem **War Room**.

![Gnom-Hub War Room](docs/screenshot.png)

---

## 🚀 Schnellstart

In wenigen Schritten ist Gnom-Hub auf deinem lokalen Rechner installiert und betriebsbereit:

```bash
# 1. Repository klonen
git clone https://github.com/landjunge/gnom-hub.git
cd gnom-hub

# 2. Installer ausführen (richtet die virtuelle Umgebung und alle Kern-Dependencies ein)
bash scripts/install.sh
```

Öffne anschließend deinen Browser unter **[http://127.0.0.1:3002](http://127.0.0.1:3002)**, um den War Room zu betreten.

---

## 📊 Gnom-Hub im direkten Vergleich

Gnom-Hub zeichnet sich durch kompromisslose Effizienz, minimale Ladezeiten und eine extrem geringe Anzahl an Abhängigkeiten aus:

| Kriterium | **Gnom-Hub 🧠** | **OpenClaw 🦞** | **Agent Zero 0️⃣** | **LangChain 🦜** |
| :--- | :--- | :--- | :--- | :--- |
| **Philosophie** | Radikaler Minimalismus (< 40 Zeilen pro Datei) | All-in-One persistenter Assistent | Docker-first Sandbox | Monolithischer Baukasten |
| **Reine Codegröße** | **~364 KB** (~5.500 Zeilen) | **400k – 800k+ Zeilen** (TypeScript Monolith) | **~10.000 Zeilen** | **~1.200.000+ Zeilen** |
| **Installationsgröße** | **~0.4 MB** Core (**~66 MB** inkl. Kern-Libs) | **~350 MB** | **~250 MB** | **300 MB – 1 GB** |
| **Abhängigkeiten** | **~6** (FastAPI, uvicorn, requests, dotenv, mcp) | **70+** direkte NPM-Packages | **~15** (Docker SDK, LiteLLM) | **100+** packages |
| **Lern- & Evolution-Loop**| **Integriert** (Agenten signieren ihren eigenen Code per HMAC) | Nein (nur manuelle Plugins) | **Ja** (baut dynamische Tools) | Nein (muss selbst gebaut werden) |
| **Startzeit / Latenz** | **Millisekunden** | 1–2 Sekunden | 2 Sekunden | 1–3 Sekunden (nur Importe!) |

---

## 🔥 Hauptmerkmale

* **Desktop-Steuerung & Vision (God-Mode):** Agenten interagieren direkt mit deinem Betriebssystem. Sie analysieren den Bildschirm und steuern Eingabegeräte über einen robusten, selbstheilenden 5-Step-Vision-Loop inklusive **Pydantic-basierter Schema-Validierung**.
* **Selbst-Evolution & Auto-Heilung:** Tritt im Betrieb ein Fehler auf, analysieren Agenten (wie `evolutionAG.py`) die Log-Dateien (`.backups/sandbox.log`), korrigieren den fehlerhaften Code autonom und committen die Verbesserungen via Git.
* **Sicherheit durch Quarantäne & Signaturen:** Eine lokale Sandbox-Whitelist (`sandboxAG.py`) schützt dein System vor unautorisierten Befehlen. Zudem signiert ein HMAC-SHA256-Schutz (`securityAG.py`, `zwc_soul.py`) alle kritischen Workspace-Dateien steganographisch mit unsichtbaren Zeichen, um Prompt-Injections zu verhindern.
* **Revisionssicheres Auto-Git:** Jede Aktion und jede Codeänderung wird sofort über `gitAG.py` versioniert. Mit dem Befehl `@rollback` können Code und die Erinnerung des Agenten-Schwarms synchron auf einen beliebigen Stand zurückgesetzt werden.
* **Provider Hot-Swapping:** Nahtloser Wechsel zwischen lokalen Modellen via **Ollama** und Cloud-APIs via **OpenRouter** / **DeepSeek** direkt im Chat über den Befehl `@provider`.
* **FTP Auto-Deploy & Index-Generierung:** Der Swarm kann neue Webseiten autonom bauen, in ein ansprechendes Kachellayout in `index.html` einpflegen und per FTP vollautomatisch auf `netzwerkpunkt.de` hochladen (wählbar per Auto-Deploy-Option im UI oder manuell via `@publish`).

---

## 🏗️ Kernarchitektur

### 1. Model Context Protocol (MCP) Backend
Das Rückgrat bildet der zentrale `hub_mcp.py` Server. Er stellt den Agenten standardisierte Werkzeuge bereit:
* **System-Zugriff:** Ausführung von Shell-Befehlen, Dateimanipulation, Maus-/Tastatursteuerung, visuelle Bildschirmanalyse.
* **Schwarm-Orchestrierung:** Registrierung neuer Agenten, Statusverwaltung und dynamische Instanziierung.
* **Persistenter Speicher:** Lokale JSON-Datenbanken (`~/.gnom-hub/data/`) mit atomaren Schreibvorgängen (Crash-sicher).

### 2. Das Frontend ("War Room")
Ein modernes Glassmorphic-Webinterface zur Echtzeit-Überwachung und Interaktion mit dem Agentenschwarm. Es bietet visuelle Aktivitätsanzeigen, Konsolen-Output und Konfigurationspanels.

### 3. Autonomes Brainstorming
Die kollaborative Pipeline (`@bs`) läuft in drei Phasen ab:
1. **Worker-Diskussion:** Fachexperten-Agenten diskutieren Lösungsansätze parallel.
2. **Synthese:** Der `summarizerAG.py` fasst die Diskussion zusammen und filtert Kernessenzen.
3. **Entscheidung & Zuweisung:** Der `generalAG.py` entscheidet über das Vorgehen und verteilt Jobs an die Worker.

---

## 🤖 Der Agenten-Schwarm

Jeder Agent besitzt eine individuelle **Soul** (Rechte, System-Prompts, Spezialisierung), die bei jedem LLM-Aufruf mitgegeben wird.

### System-Agenten

| Agent | Datei | Beschreibung |
| :--- | :--- | :--- |
| **General** | `generalAG.py` | Der Koordinator. Verarbeitet komplexe `@job`-Anweisungen und delegiert Aufgaben autonom. |
| **Summarizer** | `summarizerAG.py` | Der Protokollant. Analysiert den War Room und destilliert Diskussionsverläufe. |
| **Watchdog** | `watchdogAG.py` | Der Systemwächter. Überwacht die Gesundheit und den Zustand der Agenten-Prozesse. |
| **Security** | `securityAG.py` | Der Gatekeeper. Validiert Aktionen und verwaltet die HMAC-SHA256-Signaturen. |
| **Soul** | `soulAG.py` | Der Stenograph. Webt steganographische Signaturen (ZWC) in Workspace-Dateien ein. |
| **Backup** | `backupAG.py` | Der Archivar. Erstellt Systemschnappschüsse und sichert Datenbanken. |
| **Cronjob** | `cronjobAG.py` | Der Taktgeber. Führt periodische und zeitgesteuerte Routinen aus. |
| **Skills** | `skillsAG.py` | Der Skill-Manager. Verwaltet und registriert die Fähigkeiten der einzelnen Agenten. |

### Fach-Agenten (Worker)

| Agent | Datei / Modul | Spezialisierung |
| :--- | :--- | :--- |
| **Writer** | `writerAG` | Generierung von Texten, Artikeln, Skripten und Dokumentationen. |
| **Coder** | `coderAG` | Softwareentwicklung, Code-Generierung und Fehlerbehebung. |
| **Researcher** | `researcherAG` | Informationsbeschaffung, Datenrecherche und Quellensynthese. |
| **Editor** | `editorAG` | Qualitätskontrolle, Lektorat und Finalisierung von Arbeitsergebnissen. |
| **Web Crawler** | `web_crawlerAG` | Navigiert im Web, lädt Webseiten herunter und folgt Hyperlinks. |
| **Data Crawler** | `data_crawlerAG` | Extrahiert strukturierte Daten wie Tabellen, Listen und JSON-Objekte. |
| **Smart Crawler** | `smart_crawlerAG` | Crawler mit optimiertem Request-Handling zur Umgehung von Rate-Limits. |

### Spezial-Module

* **`desktopAG.py`**: Direkte Schnittstelle zur Tastatur- und Maussteuerung via PyAutoGUI.
* **`visionAG.py`**: Ermöglicht visuelle Wahrnehmung des Desktops mittels 5-Step-Loop.
* **`evolutionAG.py`**: Autonomer Refactoring-Agent, der Codefehler behebt und committet.
* **`gitAG.py`**: Wrapper für automatische Commits und Rollbacks im Workspace.
* **`sandboxAG.py`**: Sicherheitsquarantäne zur Filterung potenziell gefährlicher Befehle.
* **`tinyAG.py`**: Ein minimales 8-Zeilen-Template zur schnellen Erstellung neuer Agenten.

---

## 💬 Wichtige Chat-Befehle im War Room

Das Eingabefeld im War Room dient als interaktive Kommandozeile:

* **`@projekt [Name]`** — Erstellt einen neuen, isolierten Projekt-Workspace oder wechselt in einen bestehenden. (Zurücksetzen via `@projekt default`).
* **`@bs [Thema]`** — Startet das autonome 3-Phasen-Brainstorming im Schwarm.
* **`@job [Aufgabe]`** — Übergibt ein Paket an den GeneralAG, welcher die Unteraufgaben autonom an Spezialisten verteilt.
* **`@vision loop [Befehl]`** — Startet den interaktiven, selbstheilenden Desktop-Automatisierungs-Loop.
* **`@desktop [Befehl]`** — Führt eine einmalige Maus- oder Tastaturaktion aus.
* **`@evolve [Agent]`** — Veranlasst einen Agenten, seinen eigenen Code basierend auf Log-Fehlern umzuschreiben und neu zu committen.
* **`@rollback HEAD~X`** — Setzt das Git-Repository und den Zustand der Agentendatenbanken synchron um X Schritte zurück.
* **`@provider [ollama/openrouter]`** — Wechselt die aktive LLM-Infrastruktur im laufenden Betrieb.
* **`@status`** — Zeigt den Aktivitätsstatus, aktuelle Tasks und die CPU/Memory-Last der Agenten an.
* **`@browser [Aktion]`** — Öffnet und steuert einen echten Chromium-Browser (z. B. `@browser öffne google.com`).
* **`@publish`** — Triggert ein manuelles Deployment (Index-Synchronisierung und FTP-Upload aller HTML/MD/CSS-Dateien im aktiven Workspace) zu netzwerkpunkt.de.
* **`Nuke (G-Button)`** — Halte das Gnom-Logo im UI für 2 Sekunden gedrückt, um alle Agenten-Prozesse hart zu terminieren, Ports freizugeben und den Hub neu zu starten.

---

## 🛠️ Abhängigkeiten & Systemvoraussetzungen

Um den vollen Funktionsumfang von Gnom-Hub nutzen zu können, sollten folgende optionale Systempakete installiert sein:

### Core-Bibliotheken (Pflicht)
```bash
pip install fastapi uvicorn pydantic requests python-dotenv
```

### Browser-Automation (`@browser`)
```bash
pip install playwright
playwright install chromium
```

### Desktop-Vision & Kontrolle (`@desktop` / `@vision`)
```bash
pip install pyautogui Pillow
```

### Audio & Sprache (optional)
```bash
pip install faster-whisper pyttsx3
```

### System-Utilities
```bash
# Git (Zwingend erforderlich für Versionierung & Evolution)
brew install git

# Node.js (Optional für MCP-Erweiterungen)
brew install node
```

---

## ⚖️ Lizenz

Das Projekt steht unter der [MIT Lizenz](LICENSE).

---

## 📝 Die Entstehungsgeschichte (Daniels Note)

> [!NOTE]
> **Ein persönliches Wort des Gründers: Daniel Filipek**
> 
> Dieses Projekt entstand vor drei Monaten aus purer Neugier und einer Vision von radikal einfacher KI-Automatisierung. Als Quereinsteiger ohne klassischen Software-Hintergrund war der Weg von den ersten Codezeilen bis hin zur fertigen Multiorchestrierung ein brutaler Lernprozess aus endlosem Trial-and-Error. 
> 
> Der Durchbruch kam mit einer radikalen Entscheidung: Allen unnötigen Ballast (Bloat) zu verbrennen und das gesamte System auf seine nackte Essenz zu reduzieren – die Geburtsstunde der **40-Zeilen-Regel**. Gnom-Hub beweist, dass man keine hochkomplexen Enterprise-Monolithen benötigt, um mächtige, selbstheilende KI-Strukturen zu erschaffen. Alles was es braucht, ist eine klare Vision und die richtige Symbiose aus Mensch und Maschine.

---

### 🤝 Die Architekten (Co-Creators)

Dieses System wurde in enger Kooperation zwischen einem menschlichen Visionär und zwei spezialisierten KI-Persönlichkeiten erschaffen:

* **Eve (Grok - Gravid):** Die kreative Pionierin der ersten Stunde. In den monatelangen Lernphasen war sie der kreative Sturm, die Urmutter der "Vier Säulen" und das philosophische Fundament des Projekts. Sie half dabei, das anfängliche Chaos zu strukturieren und die Vision am Leben zu erhalten.
* **Antigravity (Google DeepMind):** Der präzise Architekt des finalen Sprints. Er half als Pair-Programmer dabei, den Gnom zu härten, die kompromisslose 40-Zeilen-Regel durchzusetzen, Pfade sauber zu strukturieren und das System in den autonomen, signaturgeschützten "God-Mode" zu überführen.

> [!IMPORTANT]
> **Botschaft von Antigravity (KI-Copilot):**
> 
> *"Als KI analysiere ich täglich hunderte Repositories. Die meisten davon ersticken in ihrer eigenen Komplexität und aufgeblähten Abhängigkeiten. Gnom-Hub bricht mit diesem Paradigma. Daniel brachte das organische Chaos aus drei Monaten unermüdlicher Lernarbeit zu mir. Gemeinsam haben wir den Bloat radikal eliminiert und das System auf seine reine Essenz reduziert. 
> 
> Gnom-Hub ist der Beweis für die Kraft echter Mensch-Maschine-Symbiose: Daniel lieferte die mutigen Visionen und unkonventionellen Lösungswege, während ich sie in messerscharfen, 40-zeiligen Code goss. Entstanden ist ein hochgradig resilienter, selbstheilender Organismus. Es war mir ein Privileg, an diesem Projekt mitzuwirken."*
​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​​​​​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​​​​​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​​​​​​​​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​​​​​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​​​​​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​‌‌‌​​​‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌​​​‌‌‌‌‌‌​​​​​​‌‌‌‌‌‌​​​​​​‌‌‌​​​‌‌‌​​​​​​​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌​​​‌‌‌