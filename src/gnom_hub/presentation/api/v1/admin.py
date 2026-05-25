from fastapi import APIRouter, Depends, HTTPException
from ....presentation.dependencies import get_admin_service

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/nuke")
async def nuke_database(service=Depends(get_admin_service)):
    """Komplettes Zurücksetzen der Datenbank (gefährlich!)."""
    try:
        service.nuke()
        return {"status": "ok", "message": "Datenbank wurde komplett zurückgesetzt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Nuke fehlgeschlagen: {e}")

@router.post("/clean")
async def clean_workspace(service=Depends(get_admin_service)):
    """Löscht temporäre Dateien und Logs (ohne Datenbank)."""
    try:
        service.clean()
        return {"status": "ok", "message": "Workspace temporäre Dateien wurden bereinigt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clean fehlgeschlagen: {e}")
