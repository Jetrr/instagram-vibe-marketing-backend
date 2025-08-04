# services/carousel_service.py

import httpx
from fastapi import HTTPException
from typing import List, Optional
from schemas.instagram_post import PostCarouselRequest

INSTAGRAM_BASE_URL = "https://graph.facebook.com/v19.0"

async def upload_carousel_image(ig_id: str, image_url: str, access_token: str) -> str:
    url = f"{INSTAGRAM_BASE_URL}/{ig_id}/media"
    payload = {
        "image_url": image_url,
        "is_carousel_item": "true",
        "access_token": access_token
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(url, data=payload)
        data = resp.json()
    if resp.status_code != 200 or not data.get("id"):
        raise HTTPException(status_code=500, detail=f"Failed to upload image {image_url}: {data}")
    return data["id"]

async def create_carousel_container(ig_id: str, children_ids: List[str], access_token: str, caption: str, collaborators: Optional[List[str]] = None) -> str:
    url = f"{INSTAGRAM_BASE_URL}/{ig_id}/media"
    payload = {
        "caption": caption,
        "children": ",".join(children_ids),
        "media_type": "CAROUSEL",
        "access_token": access_token
    }
    if collaborators:
        payload["collaborators"] = ",".join(collaborators)
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(url, data=payload)
        data = resp.json()
    if resp.status_code != 200 or not data.get("id"):
        raise HTTPException(status_code=500, detail=f"Failed to create carousel container: {data}")
    return data["id"]

async def publish_carousel(ig_id: str, creation_id: str, access_token: str) -> dict:
    url = f"{INSTAGRAM_BASE_URL}/{ig_id}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(url, data=payload)
        data = resp.json()
    if resp.status_code != 200 or not data.get("id"):
        raise HTTPException(status_code=500, detail=f"Failed to publish carousel post: {data}")
    return data

async def post_instagram_carousel(payload: PostCarouselRequest):
    ig_id = payload.IG_ID
    access_token = payload.access_token
    caption = payload.caption
    content = payload.content
    collaborators = [c.strip() for c in payload.collaborators.split(",")] if payload.collaborators else None

    # flatten the image urls
    image_urls = []
    for entry in content:
        if entry.img_url:
            image_urls.append(entry.img_url)
        for c in entry.carousal:
            if c.img_url:
                image_urls.append(c.img_url)
    if len(image_urls) < 2:
        raise HTTPException(status_code=400, detail="A carousel requires at least 2 images.")

    media_ids = []
    for url in image_urls:
        media_id = await upload_carousel_image(ig_id, url, access_token)
        media_ids.append(media_id)

    creation_id = await create_carousel_container(ig_id, media_ids, access_token, caption, collaborators)
    publish_resp = await publish_carousel(ig_id, creation_id, access_token)
    return {
        "success": True,
        "publish_response": publish_resp,
        "media_ids": media_ids
    }