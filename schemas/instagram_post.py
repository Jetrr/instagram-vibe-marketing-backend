from typing import List, Optional
from pydantic import BaseModel, Field

class CarousalItem(BaseModel):
    img_url: str

class ContentObject(BaseModel):
    img_url: str
    carousal: List[CarousalItem]

class PostCarouselRequest(BaseModel):
    IG_ID: str = Field(..., description="Instagram User ID")
    access_token: str = Field(..., description="Instagram Access Token")
    caption: str = Field(..., description="Post caption")
    content: List[ContentObject] = Field(..., description="List of content")
    collaborators: Optional[str] = Field(None, description="Comma-separated list of collaborator IG IDs")