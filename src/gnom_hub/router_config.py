import os
from dotenv import load_dotenv
_env = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config", ".env")
if os.path.exists(_env): load_dotenv(dotenv_path=_env)

# === KEYS ===
OR_KEY = os.getenv("OPENROUTER_KEY_FREE_1")
DS_KEY = os.getenv("DEEPSEEK_API_KEY")

# === FREIE MODELLE — Zuordnung nach Eve (Mai 2026) ===
AGENT_MODELS = {
    # ── Kommando & Analyse (brauchen starkes Reasoning) ──
    "generalag":        ["deepseek/deepseek-v4-flash:free"],
    "watchdogag":       ["openai/gpt-oss-120b:free"],
    "securityag":       ["openai/gpt-oss-120b:free"],
    # ── Code (braucht Code-Spezialist) ──
    "coderag":          ["qwen/qwen3-coder:free"],
    # ── Recherche (braucht Thinking) ──
    "researcherag":     ["arcee-ai/trinity-large-thinking:free"],
    # ── Text (braucht guten Schreibstil) ──
    "writerag":         ["minimax/minimax-m2.5:free"],
    "editorag":         ["minimax/minimax-m2.5:free"],
}
DEFAULT_MODELS = ["deepseek/deepseek-v4-flash:free", "openai/gpt-oss-120b:free", "minimax/minimax-m2.5:free"]

def get_key_for(agent_name):
    """Holt den OpenRouter-Key für den Agenten."""
    return OR_KEY
