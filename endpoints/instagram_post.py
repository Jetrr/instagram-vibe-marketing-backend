# endpoints/carousel.py

from fastapi import APIRouter
from schemas.instagram_post import PostCarouselRequest, PostVideoCarouselRequest
from services.instagram_service import post_instagram_carousel, post_instagram_video_carousel

router = APIRouter()

@router.post("/post_carousel")
async def instagram_carousel_api(payload: PostCarouselRequest):
    return await post_instagram_carousel(payload)

@router.post("/post_video_carousel")
async def instagram_video_carousel_api(payload: PostVideoCarouselRequest):
    return await post_instagram_video_carousel(payload)