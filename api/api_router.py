from fastapi import APIRouter
from endpoints import carousel, instagram_post, persona

api_router = APIRouter()

api_router.include_router(persona.router, prefix="/persona", tags=["Persona"])
api_router.include_router(carousel.router, prefix="/carousel", tags=["Carousel"])
api_router.include_router(instagram_post.router, prefix="/instagram", tags=["Instagram"])
