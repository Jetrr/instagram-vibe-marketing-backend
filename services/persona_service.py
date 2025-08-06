from google.cloud import firestore
from typing import List, Dict
from schemas.persona import ContentHistoryEntry

db = firestore.Client(project='jetrr-ai-agent')

def fetch_persona(persona_id: str) -> dict:
    doc_ref = db.collection('persona').document(persona_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise ValueError("Persona not found")
    return doc.to_dict()