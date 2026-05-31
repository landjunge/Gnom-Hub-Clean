from fastapi import APIRouter, Depends, HTTPException, Request
from gnom_hub.core.security.hmac_signer import _get_or_create_secret
from gnom_hub.api.dependencies import get_admin_service

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/nuke")
async def nuke_database(request: Request, service=Depends(get_admin_service)):
    """Komplettes Zurücksetzen der Datenbank (gefährlich!)."""
    if request.client and request.client.host not in ("127.0.0.1", "::1", "localhost") and request.headers.get("X-Hub-Secret") != _get_or_create_secret().hex():
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        service.nuke()
        return {"status": "ok", "message": "Datenbank wurde komplett zurückgesetzt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Nuke fehlgeschlagen: {e}")

@router.post("/clean")
async def clean_workspace(request: Request, service=Depends(get_admin_service)):
    """Löscht temporäre Dateien und Logs (ohne Datenbank)."""
    if request.client and request.client.host not in ("127.0.0.1", "::1", "localhost") and request.headers.get("X-Hub-Secret") != _get_or_create_secret().hex():
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        service.clean()
        return {"status": "ok", "message": "Workspace temporäre Dateien wurden bereinigt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clean fehlgeschlagen: {e}")
