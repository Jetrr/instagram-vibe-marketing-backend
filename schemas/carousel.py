from typing import List, Optional
from pydantic import BaseModel

# More explicit slide fields for best control
class SlideContent(BaseModel):
    # For intro/cover slide (only first slide needs these)
    cover_title: Optional[str] = None
    cover_subtitle: Optional[str] = None

    # For simple text-based slides (category_2 etc)
    content: Optional[str] = None
    end_title: Optional[str] = None  # For last slide

    # For myth slides, these must be set for myth/truth slides
    myth_title: Optional[str] = None
    myth_quote: Optional[str] = None
    truth_label: Optional[str] = None
    truth_body: Optional[str] = None

class CarouselRequest(BaseModel):
    character: str  # e.g., "category_1"
    slides: List[SlideContent]

class CarouselResponse(BaseModel):
    slide_urls: List[str]


    