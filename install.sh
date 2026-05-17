#!/bin/bash
# ═══════════════════════════════════════════
#  GNOM-HUB — Installation
# ═══════════════════════════════════════════
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.gnom-hub/data"
LOG_DIR="$HOME/.gnom-hub/logs"
VENV_DIR="$REPO_DIR/.venv"

echo ""
echo "  ██████╗  ███╗   ██╗ ██████╗ ███╗   ███╗"
echo " ██╔════╝  ████╗  ██║██╔═══██╗████╗ ████║"
echo " ██║  ███╗ ██╔██╗ ██║██║   ██║██╔████╔██║"
echo " ██║   ██║ ██║╚██╗██║██║   ██║██║╚██╔╝██║"
echo " ╚██████╔╝ ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║"
echo "  ╚═════╝  ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝"
echo "              INSTALLER"
echo " ─────────────────────────────"
echo ""

# 1. Python-Version prüfen
echo "▸ Python prüfen..."
if ! command -v python3 &>/dev/null; then
    echo "✗ Python 3 nicht gefunden. Bitte installieren: brew install python3"
    exit 1
fi
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "  Python $PY_VER ✓"

# 2. Virtuelle Umgebung
echo "▸ Virtuelle Umgebung..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "  .venv erstellt ✓"
else
    echo "  .venv existiert ✓"
fi
source "$VENV_DIR/bin/activate"

# 3. Dependencies installieren
echo "▸ Dependencies installieren..."
pip install -q -e "$REPO_DIR"
echo "  Dependencies installiert ✓"

# 4. Datenverzeichnisse anlegen
echo "▸ Datenverzeichnisse..."
mkdir -p "$DATA_DIR" "$LOG_DIR" "$HOME/.gnom-hub/run"
echo "  $DATA_DIR ✓"
echo "  $LOG_DIR ✓"

# 5. .env prüfen
if [ ! -f "$REPO_DIR/.env" ]; then
    echo "▸ .env erstellen..."
    cat > "$REPO_DIR/.env" <<'EOF'
# Gnom-Hub Konfiguration
# Mindestens einen Key setzen:

# OpenRouter (kostenlose Modelle)
# OPENROUTER_KEY_FREE_1=sk-or-...
# OPENROUTER_KEY_FREE_2=sk-or-...

# DeepSeek (bezahlter Fallback)
# DEEPSEEK_API_KEY=sk-...

# Hub-Port (Standard: 3002)
# GNOM_HUB_PORT=3002
EOF
    echo "  .env Template erstellt — Keys eintragen! ✓"
else
    echo "  .env existiert ✓"
fi

# 6. Leere Datenbanken anlegen (falls neu)
echo "▸ Datenbanken prüfen..."
for db in memory chat jobs ideas tokens tools domains; do
    if [ ! -f "$DATA_DIR/$db.json" ]; then
        echo "[]" > "$DATA_DIR/$db.json"
        echo "  $db.json erstellt (leer) ✓"
    fi
done
# agents.json wird automatisch beim ersten Start via db.py geseedet

# 7. gnom-hub Command prüfen
echo "▸ CLI prüfen..."
if command -v gnom-hub &>/dev/null; then
    echo "  'gnom-hub' Command verfügbar ✓"
else
    echo "  CLI über: source .venv/bin/activate && python -m gnom_hub"
fi

echo ""
echo " ═══════════════════════════════════════════"
echo "  ✅ Installation abgeschlossen!"
echo " ═══════════════════════════════════════════"
echo ""
echo "  Starten:    source .venv/bin/activate && python -m gnom_hub"
echo "  Agenten:    bash start_agents.sh"
echo "  Frontend:   http://127.0.0.1:3002"
echo ""
echo "  ⚠️  Vergiss nicht, API-Keys in .env einzutragen!"
echo ""
