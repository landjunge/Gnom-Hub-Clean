from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from pydantic import BaseModel
from ....presentation.dependencies import get_chat_service

class BrainstormRequest(BaseModel):
    agent_ids: List[UUID]
    topic: str
    rounds: int = 3

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send")
async def send_message(agent_id: UUID, content: str, service=Depends(get_chat_service)):
    """Sendet eine Nachricht an einen Agenten."""
    try:
        message = await service.send_message(agent_id, content)
        return {"status": "ok", "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/brainstorm")
async def brainstorm(req: BrainstormRequest, service=Depends(get_chat_service)):
    """Führt paralleles Brainstorming durch."""
    try:
        messages = await service.brainstorm(req.agent_ids, req.topic, req.rounds)
        return {"status": "ok", "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
