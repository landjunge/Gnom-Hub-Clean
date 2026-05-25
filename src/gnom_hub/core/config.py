import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

HOME = Path(os.getenv("GNOM_HUB_HOME", Path.home() / ".gnom-hub"))
DATA_DIR = HOME / "data"
RUN_DIR = HOME / "run"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WORKSPACE_DIR = PROJECT_ROOT / "gnom_workspace"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
CONFIG_DIR = PROJECT_ROOT / "config"
TOKENS_FILE = CONFIG_DIR / ".gnom-hub-tokens.json"
DB_PATH = DATA_DIR / "gnomhub.db"

for d in (DATA_DIR, RUN_DIR, WORKSPACE_DIR, CONFIG_DIR): d.mkdir(parents=True, exist_ok=True)

class Config:
    BASE_DIR = PROJECT_ROOT
    DATA_DIR = DATA_DIR
    LOG_DIR = DATA_DIR / "logs"
    WORKSPACE_DIR = WORKSPACE_DIR
    DB_PATH = DB_PATH
    DB_ECHO = os.getenv("DB_ECHO", "False").lower() == "true"
    DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "ollama")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    PID_DIR = RUN_DIR
    ENABLE_WORKSPACE_SANDBOX = os.getenv("ENABLE_WORKSPACE_SANDBOX", "True").lower() == "true"

Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
