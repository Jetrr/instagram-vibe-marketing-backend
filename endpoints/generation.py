from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from schemas.generation import ImageGenerationResponse
from services.generation_service import GenerationService, fetch_and_upload_image

router = APIRouter()

@router.post("/image", response_model=ImageGenerationResponse)
async def edit_sample_image(
    prompt: str = Form(...),
    n: int = Form(1),
    size: str = Form("1024x1024"),
    quality: str = Form("high"),
    background: str = Form("auto"),
    model: str = Form("gpt-image-1"),
):
    """
    Endpoint to edit/generate an image using a fixed sample image.
    """
    sample_image_path = "./assets/sample/sample1.png"
    return await GenerationService.openai_image_edit(
        image=sample_image_path,
        prompt=prompt,
        n=n,
        size=size,
        quality=quality,
        background=background,
        model=model,
        mask=None,
    )

#video 

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.generation_service import VertexVideoService


class VideoFromImageRequest(BaseModel):
    prompt: str
    image_url: str
    output_gcs_uri: str
    aspect_ratio: str = "16:9"


@router.post("/video/generate")
def generate_video_from_image(req: VideoFromImageRequest):
    try:
        result = VertexVideoService.generate_video_from_image_pipeline(
            prompt=req.prompt,
            image_url=req.image_url,
            output_gcs_uri=req.output_gcs_uri,
            aspect_ratio=req.aspect_ratio,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))