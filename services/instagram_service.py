# services/carousel_service.py
import asyncio
import httpx
from fastapi import HTTPException
from typing import List, Optional
from schemas.instagram_post import PostCarouselRequest
import os
import tempfile

INSTAGRAM_BASE_URL = "https://graph.facebook.com/v19.0"

#IMAGE

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

#VIDEO

# async def upload_carousel_video_only(ig_id: str, video_url: str, access_token: str) -> str:
#     url = f"{INSTAGRAM_BASE_URL}/{ig_id}/media"
#     payload = {
#         "is_carousel_item": "true",
#         "access_token": access_token
#     }
#     if video_url:      # only add if present
#         payload["video_url"] = video_url

#     async with httpx.AsyncClient(timeout=60.0) as client:
#         resp = await client.post(url, data=payload)
#         data = resp.json()
#     if resp.status_code != 200 or not data.get("id"):
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Failed to upload video {video_url}: {data.get('error', data)}"
#         )

#     # Poll for video completion/transcoding
#     await poll_video_container_status(data["id"], access_token)
#     return data["id"]

# async def poll_video_container_status(container_id: str, access_token: str, max_wait: int = 60):
#     url = f"{INSTAGRAM_BASE_URL}/{container_id}?fields=status_code,status&access_token={access_token}"
#     async with httpx.AsyncClient(timeout=20.0) as client:
#         for _ in range(max_wait // 2):
#             resp = await client.get(url)
#             res_data = resp.json()
#             status_code = res_data.get("status_code")
#             status_reason = res_data.get("status")
#             if status_code == "FINISHED":
#                 return
#             if status_code == "ERROR":
#                 raise HTTPException(
#                     status_code=500, 
#                     detail=f"Instagram video processing failed. Reason: {status_reason}, IG data: {res_data}"
#                 )
#             await asyncio.sleep(2)
#     raise HTTPException(status_code=504, detail="Timed out waiting for IG video processing.")

# # async def post_instagram_video_carousel(payload):
# #     ig_id = payload.IG_ID
# #     access_token = payload.access_token
# #     caption = payload.caption
# #     collaborators = [c.strip() for c in payload.collaborators.split(",")] if payload.collaborators else None

# #     # Get list of video urls from payload
# #     video_urls = [item.vid_url for item in payload.content if item.vid_url]
# #     if len(video_urls) < 2:
# #         raise HTTPException(status_code=400, detail="A carousel requires at least 2 videos.")

# #     media_ids = []
# #     for url in video_urls:
# #         try:
# #             media_id = await upload_carousel_video_only(ig_id, url, access_token)
# #         except HTTPException as ex:
# #             # Enhanced log for failed video upload/transcoding with video url context
# #             raise HTTPException(status_code=ex.status_code, detail=f"Error with video {url}: {ex.detail}")
# #         media_ids.append(media_id)

# #     # Create the carousel parent container
# #     try:
# #         creation_id = await create_carousel_container(ig_id, media_ids, access_token, caption, collaborators)
# #     except Exception as ex:
# #         raise HTTPException(status_code=500, detail=f"Failed to create parent carousel container: {ex}")

# #     # Publish the parent container (NOT any child IDs!).
# #     try:
# #         publish_resp = await publish_carousel(ig_id, creation_id, access_token)
# #     except Exception as ex:
# #         raise HTTPException(status_code=500, detail=f"Failed to publish parent carousel: {ex}")

# #     return {
# #         "success": True,
# #         "publish_response": publish_resp,
# #         "media_ids": media_ids
# #     }



# import httpx

# UPLOAD_URL = "https://create-container-ids-instagram-527171326055.europe-west1.run.app/upload_ig_videos"
# FINALIZE_URL = "https://upload-container-to-instagram-527171326055.europe-west1.run.app/finalize_post"

# async def post_instagram_video_carousel(payload):
#     ig_id = payload.IG_ID
#     access_token = payload.access_token
#     caption = payload.caption
#     collaborators = [c.strip() for c in payload.collaborators.split(",")] if payload.collaborators else []

#     video_urls = [item.vid_url for item in payload.content if item.vid_url]
#     if len(video_urls) < 2:
#         raise HTTPException(status_code=400, detail="A carousel requires at least 2 videos.")

#     # 1. Step one: Upload all videos to get container IDs
#     upload_data = {
#         "IG_ID": ig_id,
#         "access_token": access_token,
#         "caption": caption,
#         "urls": video_urls
#     }

#     async with httpx.AsyncClient(timeout=120.0) as client:
#         upload_resp = await client.post(UPLOAD_URL, json=upload_data)
#     if upload_resp.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Video/container upload failed: {upload_resp.text}")

#     upload_result = upload_resp.json()
#     container_ids = upload_result.get("container_ids")
#     if not container_ids or len(container_ids) != len(video_urls):
#         raise HTTPException(status_code=500, detail=f"Failed to get container IDs: {upload_result}")

#     # 2. Step two: Finalize/publish the carousel post
#     finalize_data = {
#         "IG_ID": ig_id,
#         "access_token": access_token,
#         "container_ids": container_ids,
#         "caption": caption,
#         "collaborators": collaborators
#     }

#     async with httpx.AsyncClient(timeout=60.0) as client:
#         finalize_resp = await client.post(FINALIZE_URL, json=finalize_data)
#     if finalize_resp.status_code != 200:
#         raise HTTPException(status_code=500, detail=f"Finalize post failed: {finalize_resp.text}")

#     return {
#         "success": True,
#         "upload_response": upload_result,
#         "finalize_response": finalize_resp.json(),
#         "container_ids": container_ids
#     }

import httpx
import asyncio
import time

INSTAGRAM_BASE_URL = "https://graph.facebook.com/v19.0"

# STEP 1. Create child video container for each video to get rupload URI
async def create_rupload_video_container(ig_id: str, access_token: str) -> dict:
    url = f"{INSTAGRAM_BASE_URL}/{ig_id}/media"
    payload = {
        "media_type": "VIDEO",
        "upload_type": "resumable",
        "access_token": access_token
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload)
        data = resp.json()
    if "id" not in data or "uri" not in data:
        raise HTTPException(status_code=500, detail=f"Error getting rupload uri: {data}")
    return data

# STEP 2. Upload your actual video from GCS via rupload endpoint/headers
async def perform_rupload_to_instagram(rupload_uri: str, access_token: str, file_url: str):
    headers = {
        "Authorization": f"OAuth {access_token}",
        "file_url": file_url
    }
    async with httpx.AsyncClient(timeout=300.0) as client:
        resp = await client.post(rupload_uri, headers=headers)
        data = resp.json()
    if "success" not in data or not data["success"]:
        raise HTTPException(status_code=500, detail=f"Video rupload failed: {data}")
    return data

# STEP 3. Poll until video is processed and ready
async def poll_container_status(container_id: str, access_token: str, what="child",
                              max_wait: int = 600, poll_interval: float = 2.0):
    """
    Waits for Instagram container to be processed (status_code == FINISHED).
    Raises on IG error or timeout.
    @param what: "child" or "parent" -- for log output
    """
    url = f"{INSTAGRAM_BASE_URL}/{container_id}?fields=status_code,status&access_token={access_token}"
    t0 = time.monotonic()
    async with httpx.AsyncClient(timeout=20.0) as client:
        for i in range(int(max_wait // poll_interval)):
            resp = await client.get(url)
            data = resp.json()
            status_code = data.get("status_code")
            status_txt = data.get("status")
            print(f"[POLL][{what}] {container_id}: {status_code} {status_txt}")
            if status_code == "FINISHED":
                print(f"-- IG {what} {container_id} is FINISHED after {time.monotonic()-t0:.2f}s.")
                return
            if status_code == "ERROR":
                raise HTTPException(
                    status_code=500,
                    detail=f"Instagram {what} processing failed. Reason: {status_txt}. IG: {data}"
                )
            await asyncio.sleep(poll_interval)
    raise HTTPException(status_code=504, detail=f"Timed out waiting for IG {what} processing.")

async def post_instagram_video_carousel(payload):
    ig_id = payload.IG_ID
    access_token = payload.access_token
    caption = payload.caption
    collaborators = [c.strip() for c in payload.collaborators.split(",")] if payload.collaborators else None

    video_urls = [item.vid_url for item in payload.content if item.vid_url]
    if len(video_urls) < 2:
        raise HTTPException(status_code=400, detail="A carousel requires at least 2 videos.")

    media_ids = []
    for gcs_url in video_urls:
        # Get rupload uri and ids from previous code
        meta = await create_rupload_video_container(ig_id, access_token)
        container_id = meta["id"]
        rupload_uri = meta["uri"]

        await perform_rupload_to_instagram(rupload_uri, access_token, gcs_url)
        # Dynamically wait for IG to mark container as FINISHED
        await poll_container_status(container_id, access_token, what="child")
        media_ids.append(container_id)

    # Now, ready to assemble parent
    creation_id = await create_carousel_container(ig_id, media_ids, access_token, caption, collaborators)

    # Extra: Optionally poll the parent container too before publish
    # (rarely needed, but helps with large carousels or heavy load)
    try:
        await poll_container_status(creation_id, access_token, what="parent", max_wait=180)
    except Exception as exc:
        print("Parent polling failed or timed out, will attempt to publish anyway...")
        # You may want to not raise here, as often parent "catches up" after /media_publish is called

    # creation_id = await create_carousel_container(ig_id, media_ids, access_token, caption, collaborators)
    for attempt in range(5):
            try:
                publish_resp = await publish_carousel(ig_id, creation_id, access_token)
            except HTTPException as exc:
                detail = str(exc.detail)
                if ("is_transient" in detail or "code': 2" in detail) and attempt + 1 < 3:
                    print(f"Transient IG error on publish, retrying in 5s... ({attempt+1}/{3})")
                    await asyncio.sleep(5)
                    continue
                raise
            
    return {
        "success": True,
        "publish_response": publish_resp,
        "media_ids": media_ids
    }