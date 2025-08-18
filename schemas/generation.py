# schemas/generation.py
from pydantic import BaseModel
from typing import List

class ImageGenerationResponse(BaseModel):
    images: List[str]  # List of URLs
    mime_type: str = "image/png"
    metadata: dict

class ImageEditRequest(BaseModel):
    prompt: str
    n: int
    size: str
    quality: str
    background: str
    model: str