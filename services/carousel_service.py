# services/carousel_service.py

from PIL import Image
from schemas.carousel import CarouselRequest
import importlib
from io import BytesIO

def create_carousel(payload: CarouselRequest):
    character = payload.character.lower()
    style_module = importlib.import_module(f"styles.{character}")
    print(f"Using style module: {style_module}")
    if character=='category_1':
        render_slide = style_module.render_slide
    elif character=='category_2':
        render_slide = style_module.render_slide
    else:
        raise ValueError(f"Unsupported character style: {character}")
    
    images_data = []
    for idx, slide in enumerate(payload.slides):
        slide_img = render_slide(slide, idx)
        img_bytes = BytesIO()
        slide_img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)
        images_data.append(img_bytes)
    return images_data

