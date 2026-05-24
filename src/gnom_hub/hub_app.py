import os
import uvicorn
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .proc_mgr import start_background_agents, kill_background_agents
from .log import get_logger

from .routes_memory import router as memory_router
from .routes_agents import router as agents_router
from .routes_nudge import router as nudge_router
from .routes_registry import router as registry_router
from .routes_chat import router as chat_router
from .routes_audio import router as audio_router
from .routes_admin import router as admin_router
from .chat_commands import router as ideas_router
from .routes_workspace import router as workspace_router
from .routes_llm import router as llm_router
from .routes_llm_models import router as llm_models_router
from .routes_showbox import router as showbox_router

logger = get_logger("hub_app")

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # 1. Datenbank initialisieren
    try:
        init_db()
        logger.info("Database initialized successfully at lifespan startup.")
    except Exception as e:
        logger.critical(f"Database initialization failed during lifespan startup: {e}")
        raise e

    # 2. Hintergrund-Agenten starten (inkl. Watchdog)
    try:
        start_background_agents()
        logger.info("Background agents started successfully.")
    except Exception as e:
        logger.error(f"Failed to start background agents: {e}")

    yield

    # 4. Hintergrund-Agenten beim Shutdown beenden
    try:
        kill_background_agents()
        logger.info("Background agents stopped successfully.")
    except Exception as e:
        logger.error(f"Failed to stop background agents: {e}")

app = FastAPI(title="GNOM-HUB", lifespan=lifespan)

# CORS Middleware konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*", "http://127.0.0.1:*"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_methods=["*"],
    allow_headers=["*"]
)

# Router einbinden
for r in [
    memory_router, agents_router, nudge_router, registry_router, chat_router,
    audio_router, admin_router, ideas_router, workspace_router, llm_router,
    llm_models_router, showbox_router
]:
    app.include_router(r)

FRONT = Path(__file__).parent.parent.parent / "frontend"
if FRONT.exists():
    app.mount("/static", StaticFiles(directory=str(FRONT)), name="static")

@app.get("/")
def root():
    index_path = FRONT / "index.html"
    return FileResponse(str(index_path)) if index_path.exists() else {"message": "GNOM-HUB", "version": "0.3.0"}

@app.get("/help")
def get_help():
    help_path = FRONT / "help.html"
    return FileResponse(str(help_path)) if help_path.exists() else {"message": "GNOM-HUB Help"}

def main():
    uvicorn.run("gnom_hub.hub_app:app", host="127.0.0.1", port=int(os.environ.get("GNOM_HUB_PORT", 3002)))
