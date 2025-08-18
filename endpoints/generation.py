from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from schemas.generation import ImageGenerationResponse, ImageEditRequest
from services.generation_service import GenerationService, fetch_and_upload_image

router = APIRouter()

@router.post("/image", response_model=ImageGenerationResponse)
async def edit_sample_image(request: ImageEditRequest):
    """
    Endpoint to edit/generate an image using a fixed sample image.
    """
    sample_image_path = "./assets/sample/sample1.png"
    return await GenerationService.openai_image_edit(
        image=sample_image_path,
        prompt=request.prompt,
        n=request.n,
        size=request.size,
        quality=request.quality,
        background=request.background,
        model=request.model,
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