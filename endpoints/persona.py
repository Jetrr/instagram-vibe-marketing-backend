from fastapi import APIRouter, HTTPException
from schemas.persona import (
    AddContentHistoryRequest,
    FetchContentHistoryRequest,
    ContentHistoryResponse,
    ContentHistoryEntry
)
from services.persona_service import add_content_history, fetch_content_history
from schemas.persona import GetSystemPromptRequest, SystemPromptResponse
from services.persona_service import get_system_prompt

router = APIRouter()

@router.post("/add_content_history", response_model=dict)
def add_entry(req: AddContentHistoryRequest):
    add_content_history(req.persona_id, req.entry)
    return {"status": "success"}

@router.get("/get_content_history/{persona_id}", response_model=ContentHistoryResponse)
def get_content(persona_id: str):
    entries = fetch_content_history(persona_id)
    return ContentHistoryResponse(content_history=[ContentHistoryEntry(**e) for e in entries])

@router.get("/system_prompt")
def fetch_system_prompt(persona_id: str):
    try:
        print('---UPDATE')
        
        prompt = get_system_prompt(persona_id=persona_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return SystemPromptResponse(system_prompt=prompt)