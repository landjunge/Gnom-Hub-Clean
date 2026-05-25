import os
from dotenv import load_dotenv
from gnom_hub.core.config import CONFIG_DIR

_env = CONFIG_DIR / ".env"
if _env.exists():
    load_dotenv(dotenv_path=str(_env))

OR_KEY = os.getenv("OPENROUTER_KEY_FREE_1")
DS_KEY = os.getenv("DEEPSEEK_API_KEY")

AGENT_MODELS = {
    "generalag":        ["deepseek/deepseek-v4-flash:free"],
    "watchdogag":       ["openai/gpt-oss-120b:free"],
    "securityag":       ["openai/gpt-oss-120b:free"],
    "coderag":          ["qwen/qwen3-coder:free"],
    "researcherag":     ["arcee-ai/trinity-large-thinking:free"],
    "writerag":         ["minimax/minimax-m2.5:free"],
    "editorag":         ["minimax/minimax-m2.5:free"],
}
DEFAULT_MODELS = ["deepseek/deepseek-v4-flash:free", "openai/gpt-oss-120b:free", "minimax/minimax-m2.5:free"]

def get_key_for(agent_name):
    return OR_KEY
