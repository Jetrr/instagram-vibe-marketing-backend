# from pydantic import BaseModel
# from typing import List, Optional

# class ContentHistoryEntry(BaseModel):
#     name: str
#     system_prompt: str

# class AddContentHistoryRequest(BaseModel):
#     persona_id: str
#     entry: ContentHistoryEntry

# class FetchContentHistoryRequest(BaseModel):
#     persona_id: str

# class ContentHistoryResponse(BaseModel):
#     content_history: List[ContentHistoryEntry]

# class GetSystemPromptRequest(BaseModel):
#     persona_id: str
#     content_name: str

# class SystemPromptResponse(BaseModel):
#     system_prompt: str