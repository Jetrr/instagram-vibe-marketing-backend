from google.cloud import firestore
from typing import List, Dict
from schemas.persona import ContentHistoryEntry

db = firestore.Client(project='jetrr-ai-agent')

def add_content_history(persona_id: str, entry: ContentHistoryEntry):
    doc_ref = db.collection('persona').document(persona_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({
            "content_history": firestore.ArrayUnion([entry.dict()])
        })
    else:
        doc_ref.set({
            "content_history": [entry.dict()]
        })

def fetch_content_history(persona_id: str) -> List[Dict]:
    doc_ref = db.collection('persona').document(persona_id)
    doc = doc_ref.get()
    if not doc.exists:
        return []
    data = doc.to_dict()
    return data.get("content_history", [])

def get_system_prompt(persona_id: str) -> str:
    doc_ref = db.collection('persona').document(persona_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise ValueError("Persona not found")
    data = doc.to_dict()
    # If you store `system_prompt` at document level:
    if "system_prompt" in data:
        return data["system_prompt"]
    # Or if in first entry of content_history:
    history = data.get("content_history", [])
    if history and "system_prompt" in history[0]:
        return history[0]["system_prompt"]
    raise ValueError("No system prompt found")