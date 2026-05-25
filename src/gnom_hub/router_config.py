import os
from dotenv import load_dotenv
_env = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config", ".env")
if os.path.exists(_env): load_dotenv(dotenv_path=_env)

# === KEYS ===
OR_KEY = os.getenv("OPENROUTER_KEY_FREE_1")
DS_KEY = os.getenv("DEEPSEEK_API_KEY")

# === FREIE MODELLE — Zuordnung nach Eve (Mai 2026) ===
AGENT_MODELS = {
    "generalag":   ["meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "openai/gpt-oss-120b:free", "deepseek/deepseek-v4-flash:free"],
    "watchdogag":  ["meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "openai/gpt-oss-120b:free", "deepseek/deepseek-v4-flash:free"],
    "securityag":  ["meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "openai/gpt-oss-120b:free", "deepseek/deepseek-v4-flash:free"],
    "coderag":     ["qwen/qwen3-coder:free", "meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "deepseek/deepseek-v4-flash:free"],
    "researcherag":["arcee-ai/trinity-large-thinking:free", "meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "deepseek/deepseek-v4-flash:free"],
    "writerag":    ["minimax/minimax-m2.5:free", "meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "deepseek/deepseek-v4-flash:free"],
    "editorag":    ["minimax/minimax-m2.5:free", "meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "deepseek/deepseek-v4-flash:free"],
}
DEFAULT_MODELS = ["meta-llama/llama-3.3-70b-instruct:free", "nousresearch/hermes-3-llama-3.1-405b:free", "openai/gpt-oss-120b:free", "deepseek/deepseek-v4-flash:free"]

def get_key_for(agent_name):
    """Holt den OpenRouter-Key für den Agenten."""
    return OR_KEY
