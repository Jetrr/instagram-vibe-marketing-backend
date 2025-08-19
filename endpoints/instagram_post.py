from fastapi import APIRouter
from schemas.instagram_post import PostCarouselRequest, PostVideoCarouselRequest, PostReelRequest
from services.instagram_service import post_instagram_carousel, post_instagram_video_carousel, post_instagram_reel

router = APIRouter()

@router.post("/post_carousel")
async def instagram_carousel_api(payload: PostCarouselRequest):
    return await post_instagram_carousel(payload)

@router.post("/post_video_carousel")
async def instagram_video_carousel_api(payload: PostVideoCarouselRequest):
    return await post_instagram_video_carousel(payload)

@router.post("/post_reel")
async def instagram_reel_api(payload: PostReelRequest):
    return await post_instagram_reel(payload)