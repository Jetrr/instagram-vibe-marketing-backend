
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from schemas.carousel import CarouselRequest
from services.carousel_service import create_carousel
from io import BytesIO
import zipfile
from google.cloud import storage
import uuid
import os

router = APIRouter()
GCS_BUCKET_NAME = "vibe_marketing"  

def upload_to_gcs(image_bytes, gcs_blob_path):
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_string(image_bytes, content_type="image/png")
    # No make_public for uniform bucket ACLs!
    return f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{gcs_blob_path}"

@router.post("/", response_description="Uploads carousel images to GCS and returns URLs")
def generate_carousel_and_upload(payload: CarouselRequest):
    try:
        images = create_carousel(payload)
        urls = []
        unique_run_id = uuid.uuid4().hex
        for idx, img_bytes in enumerate(images):
            img_bytes.seek(0)
            gcs_path = f"carousel/{unique_run_id}/slide_{idx+1}.png"
            url = upload_to_gcs(img_bytes.getvalue(), gcs_path)
            urls.append(url)
        return {"folder_id": unique_run_id, "urls": urls}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/single/{slide_idx}", response_description="Returns the requested carousel image")
def generate_single_carousel_image(payload: CarouselRequest, slide_idx: int = 0):
    try:
        images = create_carousel(payload)
        if slide_idx < 0 or slide_idx >= len(images):
            raise HTTPException(404, "Slide index out of range.")
        img_bytes = images[slide_idx]
        img_bytes.seek(0)
        return StreamingResponse(img_bytes, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))