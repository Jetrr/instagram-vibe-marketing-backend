from fastapi import APIRouter, HTTPException
from services.persona_service import fetch_persona

router = APIRouter()

@router.get("/fetchPersona/{persona_id}", response_model=dict)
def get_persona(persona_id: str):
    try:
        persona = fetch_persona(persona_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return persona