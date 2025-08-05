# from fastapi import APIRouter, HTTPException
# from google.cloud import firestore
# from typing import List, Dict
# from schemas.persona import ContentHistoryEntry
# import os
# print("Credentials:", os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
# db = firestore.Client()
# print("Firestore client initialized")
# ref = db.collection('persona')
# print("Collections accessed")
# for doc in ref.stream():
#     print(doc.id, doc.to_dict())
# db = firestore.Client() 

# def add_content_history(persona_id: str, entry: ContentHistoryEntry):
#     doc_ref = db.collection('persona').document(persona_id)
#     doc = doc_ref.get()
#     if doc.exists:
#         doc_ref.update({
#             "content_history": firestore.ArrayUnion([entry.dict()])
#         })
#     else:
#         doc_ref.set({
#             "content_history": [entry.dict()]
#         })

# def fetch_content_history(persona_id: str) -> List[Dict]:
#     doc_ref = db.collection('persona').document(persona_id)
#     doc = doc_ref.get()
#     if not doc.exists:
#         return []
#     data = doc.to_dict()
#     return data.get("content_history", [])

# def get_system_prompt(persona_id: str) -> str:
#     print('---UPDATE')
#     doc_ref = db.collection('persona').document(persona_id)
#     doc = doc_ref.get()
#     if not doc.exists:
#         print("Persona not found")
#         raise ValueError("Persona not found")
#     data = doc.to_dict()
#     print("DATA", data)
#     history = data.get("content_history", [])
#     print("HISTORY", history)
#     if not history:
#         print("Empty history")
#         raise ValueError("No content history")
#     first = history[0]
#     print("FIRST ENTRY", first)
#     return first.get("system_prompt", "")

    