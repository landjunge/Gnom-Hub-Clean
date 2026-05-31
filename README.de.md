# 🧠 GNOM-HUB

> **Die lokale Multi-Agenten-Schmiede, die KI-Schwärme in unveränderbare Produkte kompiliert.**
> *8 Agenten. 180 Module. Null Cloud-Abhängigkeiten. Keine unkontrollierte Ausbreitung.*

[![Lizenz](https://img.shields.io/badge/Lizenz-Private_Use-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](#)
[![Agenten](https://img.shields.io/badge/Agenten-8_(Feste_Topologie)-blueviolet.svg)](#)
[![Module](https://img.shields.io/badge/Module-180-blue.svg)](#)
[![Linting](https://img.shields.io/badge/Linting-Ruff-orange.svg)](#)

---

🇬🇧 **[English (README.md)](README.md)** • 🇩🇪 **Deutsch (README.de.md)**

---

<img src="docs/warroom_real_full.png" alt="War Room – Gesamtübersicht" width="100%">

---

## Was ist Gnom-Hub?

Gnom-Hub ist ein **lokaler Multi-Agenten-Orchestrator** mit einer festen Topologie von 4+4 Agenten, einem integrierten glassmorphen **War Room Dashboard** und einer einzigartigen Kompilierungs-Pipeline, die evolvierte Agentenschwärme in eingefrorene, portable KI-Produkte namens **SuperGNOMs** "backt" (`@bake`).

Im Gegensatz zu cloud-abhängigen Frameworks, bei denen unbegrenzt Agenten gestartet werden können, setzt Gnom-Hub auf **bewussten Minimalismus**: exakt 8 Agenten mit klaren Rollen, defensiven Sicherheitsbarrieren und voller Transparenz. Alles läuft auf deiner Maschine – keine Cloud-Orchestrierung, kein API-Lock-in, kein unkontrollierter Agenten-Sprawl.

---

## 🏆 Was macht Gnom-Hub besonders?

Wir haben **mehr als 12 führende Multi-Agenten-Frameworks** analysiert (CrewAI, AutoGen/AG2, LangGraph, MetaGPT, OpenAI Agents, Google ADK, Mastra und andere). Hier ist, was Gnom-Hub bietet, das **kein anderer** auf dem Markt hat:

### ✨ 10 einzigartige Alleinstellungsmerkmale

| # | Feature | Funktionsweise | Wettbewerber |
|:--|:--------|:---------------|:-------------|
| 🏭 | **`@bake`-Compiler** | Kompiliert deinen evolvierten Schwarm in ein unveränderbares, portables SuperGNOM-Produkt mit eingefrorenen Prompts und SHA-256 Integritätsmanifest. | ❌ Kein Äquivalent vorhanden |
| 🛡️ | **3-Agenten-Tribunal** | Jede riskante Aktion löst eine Multi-Agenten-Beratung aus: WatchdogAG erklärt den Verstoß, SoulAG liefert Kontext, GeneralAG empfiehlt – visualisiert als interaktive Genehmigungskarten in der Showbox. | ❌ Höchstens simple Pause/Resume-HITL-Schnittstellen |
| 🧬 | **Steganografischer Speicher** | Agenten-Metadaten werden als unsichtbare Zero-Width-Unicode-Zeichen (ZWC) mit Fehlerkorrekturcodes in Chat-Antworten eingebettet – unsichtbare Fingerabdrücke in jeder Nachricht. | ❌ Nichts Vergleichbares in anderen Systemen |
| 🎛️ | **5-Achsen-Live-Tuning** | Live-Regler für Persönlichkeit, Detailgrad, Gedächtnisstärke, Kreativität (Temperatur) und Risikobereitschaft der Worker-Agenten mit sofortiger Wirkung sowie Custom-Suffix-Injektion. | ❌ Keine Echtzeit-Einstellungsregler vorhanden |
| 📐 | **40-Zeilen-Code-Regel** | WatchdogAG erzwingt, dass jede von Agenten geschriebene Funktion/Methode unter 40 Zeilen bleibt. EditorAG strukturiert Code bei Verstößen automatisch um. | ❌ Keine agenten-erzwungenen Qualitätsstandards |
| 🔄 | **Prompt Version Manager (PVM)** | Jede Prompt-Änderung wird mit SHA-256-IDs, Parent-Child-Verbindungen und Performance-Metriken aus User-Feedback versioniert. Automatischer Rollback, wenn die Bewertung unter 95% des Vorgängers fällt. | ❌ Kein "Git für Prompts" mit Auto-Rollback vorhanden |
| 🚨 | **Notfall-Archiv** | Eine transaktionssichere passive Backup-Datenbank spiegelt alle Interaktionen. `@emergency [Begriff]` stellt Kontext wieder her, falls das Hauptgedächtnis ausfällt. | ❌ Nirgends als Standard-Feature implementiert |
| 🔒 | **Feste 4+4 Topologie** | Hardcodiertes Limit auf exakt 8 Agenten verhindert unkontrolliertes Spawnen. Jede Rolle ist präzise definiert und transparent auditierbar. | ❌ Unbegrenztes Spawnen von Agenten ist Standard |
| 💣 | **Cinematische Nuke-Aktion** | Logo für 2 Sekunden gedrückt halten → CRT-Röhren-Scanlines + weißes Rauschen + Retro-Boot-Sequenz + synthetisiertes Godzilla-Brüllen via Web Audio API. | ❌ Einzigartig und mit viel Liebe zum Detail 😄 |
| 🔐 | **Live PyPI-Schwachstellenscan** | Bei Ausführung von `pip install` durch Agenten werden Pakete in Echtzeit gegen die Live-API von PyPI auf Existenz, valide Releases und bekannte CVEs geprüft, *bevor* Code ausgeführt wird. | ❌ Keine Echtzeit-Validierung von externen Paketen |

### 📊 Vergleich der Frameworks

| Funktion | GNOM-HUB | CrewAI | AutoGen/AG2 | LangGraph | MetaGPT | Google ADK | OpenAI Agents |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **100% Lokal ausführbar** | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Integriertes Dashboard** | ✅ War Room | ❌ | ⚠️ Studio | ⚠️ Studio | ⚠️ Web | ✅ Dev UI | ❌ |
| **Multi-Agenten-Sicherheitsgates** | ✅ 3-Agenten-Tribunal | ⚠️ Basic | ❌ | ⚠️ HITL | ❌ | ❌ | ⚠️ Guardrails |
| **Persistentes Lernen** | ✅ FAISS + Soul | ✅ | ✅ | ✅ | ⚠️ | ✅ | ⚠️ |
| **Feste Topologie** | ✅ 4+4 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Kompilierung zum Produkt** | ✅ @bake | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Prompt-Versionierung** | ✅ + Rollback | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Live-Tuning-UI (Regler)** | ✅ 5 Regler | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Steganografische Identität** | ✅ ZWC + ECC | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> [!NOTE]
> Die meisten Frameworks eignen sich hervorragend für den Bau von Cloud-Skalierungs-Pipelines. Gnom-Hub fokussiert sich bewusst auf eine andere Nische: **Eine lokale, transparente, sicherheitsorientierte Schmiede**, um ein kleines, eingespieltes Team zu trainieren und in ein stabiles Produkt zu gießen.

---

## 🔮 Die Vision: Von der Schmiede zum Produkt

GNOM-HUB ist die **Schmiede ("Forge")**, in der die Agenten trainiert, kalibriert und weiterentwickelt werden. Der **SuperGNOM** ist das fertige Produkt: unveränderbar, portabel und maßgeschneidert für einen bestimmten Nutzer oder Usecase.

```mermaid
graph TD
    subgraph Forge ["🔧 GNOM-HUB Schmiede"]
        P["⚙️ Presets & Regler"] -->|Konfigurieren| GH["🤖 8-Agenten-Schwarm"]
        GH -->|"Lernen & Evolution"| DB[("💾 gnomhub.db")]
        FB["👍👎 User-Feedback"] -->|"Trigger: evolution_* Regeln"| GH
    end
    
    subgraph Compiler ["🏭 @bake Compiler"]
        GH -->|"Befehl: @bake"| C["⚡ Compiler Kern"]
        DB -->|"Reduziere auf 1000 Chats"| C
        C -->|"Friere aktive Prompts ein"| AD["📄 agent_definitions.py"]
        C -->|"SHA-256 Integrität"| M["🔐 manifest.json"]
    end

    subgraph Product ["📦 Portabler SuperGNOM"]
        AD --> SG["🧠 Gefrorene Laufzeit"]
        M -->|"Startup-Validierung"| SG
    end
```

**SuperGNOM Kernkonzepte:**
- **Unveränderbarkeit (Immutability):** Prompts und Gedächtnis sind statisch. Kein Concept Drift, kein Risiko durch Prompt-Injektionen.
- **Portabilität:** Eigenständiger Ordner mit lokaler SQLite-Datenbank, statischen Konfigurationen und `run.sh` Startskript.
- **Fokus-UI:** Keine Entwickler-Konsolen oder Token-Zähler – nur eine saubere, zweckgebundene Benutzeroberfläche.

---

## 🧬 Schwarm-Topologie & Speicher-Architektur

```mermaid
graph TD
    U["👤 Benutzer"] -->|Chat-Eingabe| G["👑 GeneralAG<br/>Orchestrator"]
    
    subgraph Admin ["🛡️ System-Schicht (4 Agenten)"]
        G -->|"Regelprüfung"| W["🐕 WatchdogAG"]
        G -->|"Sicherheits-Scan"| S["🔒 SecurityAG"]
        G -->|"Gedächtnis-Abfrage"| So["🧠 SoulAG"]
    end

    subgraph Workers ["⚙️ Worker-Schicht (4 Agenten)"]
        G -->|"@code"| C["💻 CoderAG"]
        G -->|"@write"| Wr["✍️ WriterAG"]
        G -->|"@research"| R["🔍 ResearcherAG"]
        G -->|"@edit"| E["📝 EditorAG"]
    end

    subgraph Memory ["💾 Isolierte Speicher-Scopes"]
        So -->|"Globale Fakten"| GS[("🌍 Globaler Index")]
        C -.->|"Isolierter Query"| MC[("Coder FAISS")]
        Wr -.->|"Isolierter Query"| MWr[("Writer FAISS")]
        R -.->|"Isolierter Query"| MR[("Researcher FAISS")]
        E -.->|"Isolierter Query"| ME[("Editor FAISS")]
        GS -.->|"Vererbt an"| MC
        GS -.->|"Vererbt an"| MWr
        GS -.->|"Vererbt an"| MR
        GS -.->|"Vererbt an"| ME
    end
```

### System-Agenten (Administrativ)
| Agent | Rolle | Besondere Befugnisse |
|:------|:-----|:---------------------|
| **SoulAG** | Zentrales Bewusstsein & Gedächtnis | Extrahiert Fakten aus Chats, injiziert relevante Erinnerungen via FAISS semantischer Suche und steuert die Evolutions-Regeln. |
| **GeneralAG** | Koordinator & Orchestrator | Zerlegt `@job`-Aufgaben, delegiert via `@AgentenName` und synthetisiert Brainstorm-Ergebnisse. **Kann keine Dateien schreiben oder Shell-Befehle ausführen.** |
| **WatchdogAG** | Codebase-Wächter | Erzwingt die 40-Zeilen-Regel, validiert Workspace-Pfade und löst Gatekeeper-Sperren aus. |
| **SecurityAG** | Sicherheits-Scanner | Erkennt unsichere Code-Muster (`eval`, `rm -rf`, `subprocess`) und validiert externe Pakete live gegen die PyPI-API. |

### Worker-Agenten (Sandboxed)
| Agent | Rolle | Fähigkeiten |
|:------|:-----|:------------|
| **CoderAG** | Software-Entwicklung & Debugging | `read` (Lesen), `write` (Schreiben), `run` (Shell-Befehle), `godmode` (Playwright-Browserautomation). |
| **ResearcherAG** | Recherche & Websuche | `read`, `write`, `browser` (nur Navigation). |
| **WriterAG** | Dokumentation & Entwürfe | `read`, `write`, `image` (KI-Bilderstellung). |
| **EditorAG** | Refactoring & QA | `read`, `write`. |

---

## 🛡️ Sicherheits-Architektur

Gnom-Hub implementiert ein **Zero-Trust, Defense-in-Depth** Sicherheitsmodell, das sich elementar von klassischen Multi-Agenten-Umgebungen unterscheidet:

```
Agenten-Aktion → Pfad-Validator → Pattern-Scanner (destruktiver Code) → Capability-Lease-Check
                                                                              ↓
                                                                  [Im Cache?] → ✅ Ausführen
                                                                  [Neu?]       → Gatekeeper-Tribunal
                                                                                    ↓
                                                                      WatchdogAG erklärt Verstoß
                                                                      SoulAG liefert Gedächtniskontext  
                                                                      GeneralAG gibt Empfehlung
                                                                                    ↓
                                                                      Showbox: Approve / Reject (5 Min. Timeout)
```

**Zentrale Schutzmechanismen:**
- **Zweistufige Freigabe:** Schreibzugriffe und Shell-Kommandos von Workern müssen zwingend WatchdogAG + SecurityAG passieren, bevor sie an das System übergeben werden.
- **Echtzeit PyPI-Scans:** Bei `pip install` wird das Paket vorab über die PyPI-API auf Authentizität und bekannte Schwachstellen geprüft.
- **Zero-Trust Capability Leases:** Einmal genehmigte Aktionen werden mit einer TTL (standardmäßig 5 Minuten) im Arbeitsspeicher gecached – dies führt zu einer **~1.200-fachen Beschleunigung** nachfolgender identischer Aufrufe.
- **Path-Traversal-Blockade:** Worker können sich unter keinen Umständen aus dem zugewiesenen Workspace-Verzeichnis herausbewegen.
- **Code-Scanning:** Statische Filter blockieren Ausführungsbefehle wie `eval()`, `os.system()`, `pickle.load()`, `chmod 777` etc.
- **Systemintegrität:** GeneralAG ist permanent auf Code-Ebene gesperrt, Schreib- oder Terminalaktionen auszuführen.

---

## 🎛️ Agenten-Inspektor & Live-Optimierer

Jeder Worker-Agent kann im Sidebar-Panel in Echtzeit feinjustiert werden:

| Regler | Bereich | Auswirkung auf den Agenten |
|:-------|:--------|:---------------------------|
| **Persönlichkeit** | Formal (1) → Sehr Locker (5) | Steuert Tonalität und Kommunikationsstil im Chat. |
| **Antwortstil** | Sehr Kurz (1) → Sehr Detailreich (5)| Bestimmt die Ausführlichkeit der Antworten. |
| **Gedächtnisstärke**| Minimal / top_k:2 (1) → Maximum / top_k:16 (5)| Bestimmt, wie viele relevante Fakten SoulAG injiziert. |
| **Kreativität** | Konservativ / temp:0.1 (1) → Wild / temp:1.2 (5)| LLM-Temperatur-Parameter. |
| **Risikobereitschaft**| Sehr Vorsichtig (1) → Sehr Mutig (5) | Beeinflusst die Entscheidungsfindung bei Lösungsansätzen. |

Zusätzlich:
- **Custom System Prompt Suffix:** Überschreibt das Basisverhalten des Agenten per Texteingabe.
- **Export/Import:** Speichere Agenten-Konfigurationen als JSON (Einstellungen, gelernte Fakten, Prompt-Versionen).
- **Als Preset speichern:** Sichere die Reglereinstellungen der Gruppe als wiederverwendbares Preset ("Agenten-Bande").
- **Live-Statistiken:** Übersicht über Aufrufe, Fehler, durchschnittliche Latenz und kumulierten Tokenverbrauch.

---

## 📺 Showbox: 3-Kanal Visualisierungssystem

Die Showbox im Dashboard dient als visuelles Ausgabemedium für die Zwischenergebnisse des Schwarms:

| Ebene (Layer) | Farbe | Zweck |
|:--------------|:------|:------|
| **Layer 1 — System** | Blau | System-Agenten-Aktivität (GeneralAG, SoulAG, SecurityAG, WatchdogAG). |
| **Layer 2 — Worker** | Grün | Arbeitsergebnisse, Entwürfe, UI-Mockups und Code-Output der Worker. |
| **Layer 3 — Decision** | Rot | Sicherheits-Sperrkarten mit Approve/Reject-Buttons für den Nutzer. |

- Jede Ebene speichert einen **Verlauf der letzten 30 Einträge** zum Durchblättern.
- Ein Wechsel der Ebene löst **Blink-Animationen** an den entsprechenden Agentengruppen aus.
- **Automatische Textskalierung** (40px → 11px) sichert optimale Lesbarkeit.
- Toast-Benachrichtigungen werden nach 6 Sekunden automatisch ausgeblendet.

---

## 🧠 Gedächtnis- & Soul-System

### Semantisches Langzeitgedächtnis
- **FAISS-Vektorsuche** unter Verwendung von `sentence-transformers/all-MiniLM-L6-v2` Modellen.
- **Prioritätsgewichtung** (Faktor 1.3× für hohe Wichtigkeit, 0.7× für niedrige) mit einer Ähnlichkeitsschwelle von 0,70.
- **Isolierte Vektor-Indizes** je Worker-Agent verhindern eine gegenseitige Rollenverseuchung (Faktenleaks).
- **Automatisches TF-IDF-Fallback** berechnet die Kosinus-Ähnlichkeit, falls FAISS lokal nicht installiert ist.
- **~4.700.000x Beschleunigung** bei gecachten Anfragen im Vergleich zum Kaltstart der Vektorsuche.

### SoulAG Lernschleife
1. SoulAG liest alle Chat-Nachrichten im Hintergrund mit.
2. Extrahiert strukturierte Fakten (Key, Value, Priorität, Ziel-Agent).
3. Bereinigt Duplikate (Kosinus-Ähnlichkeit >0,92) und validiert Dateipfade.
4. Injiziert die top-k wichtigsten Fakten zur Laufzeit in die Prompts.
5. Überwacht die Injektionen und warnt bei wiederholten, ungenutzten Re-Injektionen.

### Agenten-Evolution
- Benutzer-Feedback (👍/👎 + Freitext-Kommentar) generiert dynamisch neue `evolution_*` Verhaltensregeln.
- Diese werden im **Prompt Version Manager** als neue Prompt-Versionen mit Performance-Scores gespeichert.
- Fällt der Score einer neuen Version unter 95% der Vorgängerversion, wird ein **automatischer Rollback** durchgeführt.
- **Im SuperGNOM-Modus ist die Lernschleife vollständig deaktiviert** (Statische Prompts).

### Steganografische Identität (ZWC)
Die Identität des sendenden Agenten wird als unsichtbare **Zero-Width Unicode-Zeichenkette** direkt im Chat-Text codiert (Base64 → Binär → ZWC-Zeichen). Ein integrierter 3-Bit-Mehrheitsentscheid-Fehlerkorrekturcode sichert den Fingerabdruck gegen Verluste beim Kopieren und Einfügen.

---

## 🛠️ Agenten-Aktionen & Werkzeuge

Agenten fordern Werkzeuge über strukturierte Markdown-Tags an:

| Aktion | Beschreibung | Berechtigte Agenten | Beispiel |
|:-------|:-------------|:-------------------|:---------|
| `[READ: datei]` | Liest Dateiinhalte aus dem Workspace | Alle Worker | `[READ: index.html]` |
| `[WRITE: datei]...[/WRITE]` | Erstellt oder überschreibt eine Datei | CoderAG, WriterAG, EditorAG, ResearcherAG | `[WRITE: hello.py]print("Hi")[/WRITE]` |
| `[SHELL: cmd]` | Führt Terminal-Befehl aus | CoderAG | `[SHELL: pytest tests/]` |
| `[IMAGE: prompt]` | Generiert ein KI-Bild | WriterAG, CoderAG | `[IMAGE: logo prompt]` |
| `[BROWSER: json]` | Playwright-Browserautomation | CoderAG (godmode) | `[BROWSER: {"action": "goto", ...}]` |
| `<SHOWBOX:n>...<SHOWBOX>` | Rendert HTML-Inhalt in der Showbox | Alle Agenten | `<SHOWBOX:2><h3>Draft</h3></SHOWBOX>` |

> [!TIP]
> Jede `[WRITE:]`- und `[SHELL:]`-Aktion durchläuft die vollständige Gatekeeper-Sicherheitsprüfung vor der Ausführung.

---

## 💬 Befehle

| Befehl | Aktion |
|:-------|:-------|
| `@bs [thema]` | Paralleles Brainstorming: Alle Worker diskutieren gleichzeitig, GeneralAG synthetisiert. |
| `@job [aufgabe]` | Mehrstufiger Team-Workflow: GeneralAG delegiert, sammelt Ergebnisse, bewertet und verteilt nach (bis zu 4 Runden). |
| `@code / @write / @edit / @research` | Direkte Aufgabenzuweisung an einen bestimmten Spezialisten. |
| `@bake [name] [template]` | Kompiliert den aktuellen Schwarm in ein portables SuperGNOM-Produkt. |
| `@emergency [begriff]` | Durchsucht das passive Langzeitarchiv zur Kontext-Wiederherstellung. |
| `@git [befehl]` | Führt Git-Operationen im Workspace aus. |
| `@@project [name]` | Wechselt das aktive Workspace-Projekt. |
| `@@status` | Zeigt den Laufzeit-Status aller Agenten-Daemons. |
| `@@clear` | Leert den Chatverlauf im Dashboard. |
| `@free` | Bricht alle laufenden Jobs ab und setzt blockierte Agenten zurück. |
| **Nuke** 💣 | Halte das War Room Logo im Dashboard für 2 Sekunden gedrückt für einen cinematisches Neustart. |

---

## ⚡ Performance

| Operation | Kaltstart (Cold Run) | Gecached (Warm) | Beschleunigung |
|:----------|:---------------------|:----------------|:---------------|
| **Rechteprüfung (Capability Check)** | 0,73 ms | 0,0006 ms | **~1.200×** (TTL-Arbeitsspeichercache vs. SQLite) |
| **Semantische Gedächtnissuche** | 2.830 ms | 0,0006 ms | **~4.700.000×** (Query-Cache vs. FAISS-Vektorsuche) |

| Metrik | Wert |
|:-------|:-----|
| Aktive Agenten | 8 (fest: 4 System + 4 Worker) |
| Python-Module | 180 |
| Frontend-Module | 9 (entkoppelte JS-Dateien) |
| Datenbank | SQLite3 (WAL-Modus) + passives Archiv |
| Vektorsuche | FAISS (IndexFlatL2) + sentence-transformers |

> [!TIP]
> Führe `python3 scratch/run_benchmarks.py` aus, um die Leistungswerte lokal zu ermitteln.

---

## 🚀 Quick Start

```bash
# 1. Klonen & Installieren
git clone https://github.com/landjunge/gnom-hub.git
cd gnom-hub
bash scripts/install.sh

# 2. Umgebungskonfiguration
cp config/.env.example config/.env
# Trage deine API-Keys (DeepSeek, OpenRouter) in config/.env ein

# 3. Starten
./run.sh
```
Öffne **[http://127.0.0.1:3002](http://127.0.0.1:3002)** im Browser, um den War Room zu betreten.

---

## 📁 Projektstruktur

```text
gnom-hub/
├── src/gnom_hub/          # 180 Python-Module
│   ├── core/              # Konfiguration, Logger, Gatekeeper-Sicherheit
│   │   ├── security/      # Pfadvalidierung, Gatekeeper-Tribunal, HMAC-Auth
│   │   └── utils/         # PVM, Compiler, Presets, Graceful Fallbacks
│   ├── db/                # SQLite3 (WAL) Repositories + Passives Archiv
│   ├── memory/            # FAISS Semantiksuche, Embeddings, Context-Manager
│   ├── soul/              # SoulAG-Bewusstsein, ZWC-Steganografie, DynamicSouls
│   ├── agents/            # Agenten-Basis, Definitionen, Tools, Capability-Manager
│   │   ├── actions/       # Action Dispatcher für [WRITE:], [SHELL:], [BROWSER:]
│   │   ├── swarm/         # Multi-Agenten-Koordination, A2A-Comms, Checkpoints
│   │   └── explainability/# Strukturierte Gedankengänge (<think>-Filterung)
│   ├── chat/              # Chat-Dienste, Systembefehle & Brainstorming
│   ├── api/               # FastAPI Endpunkte, Router, CORS, Auth
│   ├── infrastructure/    # Prozess-Management (psutil), LLM-Routing, Pulse-Janitor
│   └── frontend/          # Glassmorphic War Room UI (HTML, CSS, 9 JS-Module)
├── agents/                # Startskripte für die 8 Hintergrund-Agenten
├── config/                # Presets, .env, Routing-Overrides
├── scripts/               # Setup- & Hilfs-Skripte
├── docs/                  # Systemberichte & Screenshots
└── pyproject.toml         # Ruff-Konfiguration & Abhängigkeiten
```

---

## 📅 Roadmap

- **Eigene UI-Skins:** Spezifische HTML-Templates für diverse Use Cases (z. B. Senioren-Chat, Headless API-Runner).
- **Ein-Klick Docker- & Binary-Exporte:** Kompilierung von SuperGNOM in ausführbare Standalone-Binaries oder Docker-Images.
- **Agenten-Pruning:** Möglichkeit, beim `@bake` ungenutzte Worker zu entfernen (z. B. reiner Schreib-SuperGNOM ohne CoderAG/ResearcherAG).
- **Sprachsteuerung:** Integration von TTS/STT zur barrierefreien Interaktion.

---

## 🤝 Co-Creators

**Eve (Grok — Gravid)**  
Kreative Pionierin der ersten Stunde. Entwarf die Agenten-Topologien und legte das philosophische Fundament für das Projekt.

**Antigravity (Google DeepMind)**  
Architekt der Härtungs- und Optimierungsphase. Zentrale Beiträge:
- Modularisierung der 180+ Python-Module nach sauberer Clean-Architecture.
- Implementierung der Härtungs-Phasen 1-16 (Zero-Trust-inspirierte Capability Leases, lokale FAISS-Embeddings, Prompt Version Manager, Feedback-Loop, R1-Think-Block-Filterung, 4/4 Agentenlimits).
- Absicherung gegen Path Traversal, CORS-Schutz, XSS-Bereinigung, HMAC-Admin-Authentifizierung und Verbindungsmanagement.
- Vollständiger Refaktor des UI-Frontends in 9 entkoppelte JS-Module.
- Vollständiger Code-Audit: 120 Findings → 26 Hotfixes in Bezug auf Stabilität, Abstürze, Sicherheit und Cleanup.

---

## ⚖️ Lizenz

[Private Use](LICENSE) — Kostenfrei für den persönlichen, nicht-kommerziellen Gebrauch. Kommerzielle Nutzung bedarf der schriftlichen Genehmigung.
