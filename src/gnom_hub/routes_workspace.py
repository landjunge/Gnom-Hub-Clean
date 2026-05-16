from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os, subprocess
from .db import get_active_project

router = APIRouter()
BASE_WORKSPACE = "/Users/landjunge/Documents/AG-Flega/gnom_workspace"

def get_workspace_dir():
    d = os.path.join(BASE_WORKSPACE, get_active_project())
    os.makedirs(d, exist_ok=True)
    return d

@router.get("/api/workspace")
def list_workspace():
    wd = get_workspace_dir()
    files = []
    for f in os.listdir(wd):
        p = os.path.join(wd, f)
        if os.path.isfile(p):
            files.append({"name": f, "size": os.path.getsize(p), "mtime": os.path.getmtime(p)})
    return files

@router.get("/api/workspace/{filename}")
def read_workspace_file(filename: str):
    wd = get_workspace_dir()
    p = os.path.join(wd, filename)
    if os.path.exists(p):
        with open(p, "r") as f:
            return {"content": f.read()}
    return {"error": "File not found"}

@router.get("/api/workspace/{filename}/serve", response_class=HTMLResponse)
def serve_workspace_file(filename: str):
    """Liefert HTML/CSS/JS Dateien direkt als Webseite aus."""
    wd = get_workspace_dir()
    p = os.path.join(wd, filename)
    if not os.path.exists(p):
        return HTMLResponse("<h1>Datei nicht gefunden</h1>", status_code=404)
    with open(p, "r") as f:
        return HTMLResponse(f.read())

@router.post("/api/workspace/{filename}/run")
def run_workspace_file(filename: str):
    """Führt .py Dateien aus und gibt stdout/stderr zurück."""
    wd = get_workspace_dir()
    p = os.path.join(wd, filename)
    if not os.path.exists(p):
        return {"error": "File not found"}
    if not filename.endswith(".py"):
        return {"error": "Nur .py Dateien können ausgeführt werden."}
    try:
        r = subprocess.run(["python3", p], capture_output=True, text=True, timeout=15, cwd=wd)
        return {"stdout": r.stdout[-2000:], "stderr": r.stderr[-1000:], "code": r.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Timeout nach 15 Sekunden"}

@router.get("/api/project")
def get_project():
    return {"project": get_active_project()}
