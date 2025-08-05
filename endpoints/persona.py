from fastapi import APIRouter, HTTPException
from schemas.persona import (
    AddContentHistoryRequest,
    ContentHistoryResponse,
    ContentHistoryEntry,
    SystemPromptResponse
)
from services.persona_service import (
    add_content_history,
    fetch_content_history,
    get_system_prompt
)

router = APIRouter()

@router.post("/add_content_history", response_model=dict)
def add_entry(req: AddContentHistoryRequest):
    add_content_history(req.persona_id, req.entry)
    return {"status": "success"}

@router.get("/get_content_history/{persona_id}", response_model=ContentHistoryResponse)
def get_content(persona_id: str):
    entries = fetch_content_history(persona_id)
    return ContentHistoryResponse(content_history=[ContentHistoryEntry(**e) for e in entries])

@router.get("/system_prompt/{persona_id}", response_model=SystemPromptResponse)
def fetch_system_prompt(persona_id: str):
    try:
        prompt = get_system_prompt(persona_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return SystemPromptResponse(system_prompt=prompt)