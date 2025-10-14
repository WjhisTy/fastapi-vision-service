"""Text-to-Image API routes - Simple Demo (no PIL dependency)."""


from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/t2i", tags=["text-to-image"])


class TextToImageRequest(BaseModel):
    """Request schema for text-to-image generation."""

    prompt: str


class TextToImageResponse(BaseModel):
    """Response schema for text-to-image generation."""

    image_base64: str


# 1x1 pixel transparent PNG in base64
DEMO_IMAGE_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


@router.post("/generate", response_model=TextToImageResponse)
async def generate_image_demo(request: TextToImageRequest) -> TextToImageResponse:
    """
    DEMO: Return a test image (no real model).

    Args:
        request: Text prompt

    Returns:
        Base64 encoded test image
    """
    return TextToImageResponse(image_base64=DEMO_IMAGE_BASE64)


@router.get("/status")
async def status():
    """Demo status endpoint."""
    return {"status": "demo", "message": "Running in demo mode"}
