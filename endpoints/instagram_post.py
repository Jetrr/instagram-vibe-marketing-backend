# endpoints/carousel.py

from fastapi import APIRouter
from schemas.instagram_post import PostCarouselRequest
from services.instagram_service import post_instagram_carousel

router = APIRouter()

@router.post("/post_carousel")
async def instagram_carousel_api(payload: PostCarouselRequest):
    return await post_instagram_carousel(payload)