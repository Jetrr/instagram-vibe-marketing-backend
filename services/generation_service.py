import os

from fastapi import UploadFile, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
from typing import Union, IO
import base64
import uuid
from schemas.generation import ImageGenerationResponse

# Load .env variables if the file exists
load_dotenv()
from google.cloud import storage

GCS_BUCKET_NAME = "vibe_marketing"

def upload_to_gcs(image_bytes: bytes, gcs_blob_path: str) -> str:
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_string(image_bytes, content_type="image/png")
    return f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{gcs_blob_path}"
# Automatically use VIBE_MARKETING_OPENAI_API_KEY or OPENAI_API_KEY from env/.env
def _get_openai_api_key():
    return os.getenv("VIBE_MARKETING_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

class GenerationService:
    @staticmethod
    async def openai_image_edit(
        *,
        image: Union[str, IO],   # path or file-like object
        prompt: str,
        n: int,
        size: str,
        quality: str,
        background: str,
        model: str,
    ) -> ImageGenerationResponse:
        api_key = _get_openai_api_key()
        if not api_key:
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")

        client = OpenAI(api_key=api_key)
        try:
            if isinstance(image, str):
                image_file = open(image, "rb")
            else:
                image_file = image
                image_file.seek(0)
            

            edit_kwargs = dict(
                image=image_file,
                prompt=prompt,
                model=model,
                n=n,
                size=size,
                quality=quality,
                background=background,
            )

            resp = client.images.edit(**edit_kwargs)

        except Exception as e:
            raise HTTPException(status_code=502, detail=f"OpenAI images.edit error: {e}")
        finally:
            if isinstance(image, str):
                image_file.close()

        images_b64 = [d.b64_json for d in getattr(resp, "data", [])]
        if not images_b64:
            raise HTTPException(status_code=502, detail="OpenAI returned no images")

        urls = []
        folder = f"openai_edits/{uuid.uuid4().hex}"
        for idx, b64_str in enumerate(images_b64):
            image_bytes = base64.b64decode(b64_str)
            gcs_path = f"{folder}/edit_{idx+1}.png"
            url = upload_to_gcs(image_bytes, gcs_path)
            urls.append(url)

        return ImageGenerationResponse(
            images=urls,  
            mime_type="image/png",
            metadata={"provider": "openai", "model": model, "size": size, "n": str(n)},
        )
    
# import time
# from fastapi import HTTPException
# from google import genai
# from google.genai.types import GenerateVideosConfig, Image

# class VertexVideoService:
#     @staticmethod
#     def generate_video_from_image(
#         prompt: str,
#         image_gcs_uri: str,
#         output_gcs_uri: str,
#         aspect_ratio: str = "16:9",
#         model: str = "veo-3.0-generate-preview"
#     ) -> str:
#         client = genai.Client(
#             project="jetrr-ai-agent",
#             location="us-central1"
#         )
#         operation = client.models.generate_videos(
#             model=model,
#             prompt=prompt,
#             image=Image(
#                 gcs_uri=image_gcs_uri,
#                 mime_type="image/png",
#             ),
#             config=GenerateVideosConfig(
#                 aspect_ratio=aspect_ratio,
#                 output_gcs_uri=output_gcs_uri,
#             ),
#         )

#         while not operation.done:
#             time.sleep(15)
#             operation = client.operations.get(operation.name)
#             # Optionally log/progress here

#         if operation.response and operation.result.generated_videos:
#             return operation.result.generated_videos[0].video.uri

#         raise HTTPException(status_code=500, detail="Video generation failed.")

#video

import requests
import uuid
import time
from fastapi import HTTPException
from google.cloud import storage
from google import genai
from google.genai.types import Image, GenerateVideosConfig

GCS_BUCKET_NAME = "vibe_marketing"


def fetch_and_upload_image(image_url: str) -> (str, str):
    """
    Downloads an image from a URL and uploads to GCS.
    Returns: (gs:// uri, mime_type)
    """
    filename = image_url.split("/")[-1].split("?")[0]
    folder = f"user_image_inputs/{uuid.uuid4().hex}"
    gcs_blob_path = f"{folder}/{filename}"
    resp = requests.get(image_url)
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Unable to fetch image from {image_url} (status {resp.status_code})")
    image_bytes = resp.content
    # Infer mime type:
    ext = filename.lower().split('.')[-1]
    if ext in ["jpg", "jpeg"]:
        mime_type = "image/jpeg"
    elif ext == "png":
        mime_type = "image/png"
    else:
        mime_type = "application/octet-stream"
    upload_to_gcs(image_bytes, gcs_blob_path)
    return f"gs://{GCS_BUCKET_NAME}/{gcs_blob_path}", mime_type


from google.cloud import storage
from datetime import timedelta

def get_signed_url(bucket_name, blob_name, expiration_minutes=60):
    from google.cloud import storage
    from datetime import timedelta
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET"
    )

class VertexVideoService:
    @staticmethod
    def generate_video_from_image_pipeline(
        prompt: str,
        image_url: str,
        output_gcs_uri: str,
        aspect_ratio: str = "16:9",
        enhance_prompt: bool = True,
        generate_audio: bool = True,
        project: str = "jetrr-ai-agent",
        location: str = "us-central1"
    ) -> dict:  # <--- now returns dict
        # 1. Download image, upload to GCS
        image_gcs_uri, mime_type = fetch_and_upload_image(image_url)
        
        from google import genai
        from google.genai.types import Image, GenerateVideosConfig
        client = genai.Client(vertexai=True, project=project, location=location)

        # 2. Video Generation
        operation = client.models.generate_videos(
            model="veo-3.0-generate-preview",
            prompt=prompt,
            image=Image(gcs_uri=image_gcs_uri, mime_type=mime_type),
            config=GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                output_gcs_uri=output_gcs_uri,
                number_of_videos=1,
                duration_seconds=8,
                resolution="1080p",
                enhance_prompt=enhance_prompt,
                generate_audio=generate_audio,
            ),
        )
        while not operation.done:
            time.sleep(15)
            operation = client.operations.get(operation)
            print(operation)

        #
        import google.auth
        creds, _ = google.auth.default()
        print("Service account used:", getattr(creds, 'service_account_email', None))
        import google.cloud.storage
        print("google-cloud-storage version:", google.cloud.storage.__version__)

        if operation.response and operation.result.generated_videos:
            gcs_uri = operation.result.generated_videos[0].video.uri
            bucket, blob = gcs_uri.replace("gs://", "").split("/", 1)
            signed_url = get_signed_url(bucket, blob)
            return {
                "video_gcs_uri": gcs_uri,
                "video_signed_url": signed_url,
            }

        raise HTTPException(status_code=500, detail="Video generation failed.")