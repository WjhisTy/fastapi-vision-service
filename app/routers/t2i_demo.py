"""Text-to-Image API routes - Demo Mode (no real models)."""

import base64
import io

from fastapi import APIRouter
from PIL import Image
from pydantic import BaseModel

router = APIRouter(prefix="/t2i", tags=["text-to-image"])


class TextToImageRequest(BaseModel):
    """Request schema for text-to-image generation."""

    prompt: str


class TextToImageResponse(BaseModel):
    """Response schema for text-to-image generation."""

    image_base64: str


@router.post("/generate", response_model=TextToImageResponse)
async def generate_image_demo(request: TextToImageRequest) -> TextToImageResponse:
    """
    DEMO: Generate a simple test image (no real model).

    Args:
        request: Text prompt

    Returns:
        Base64 encoded test image
    """
    # Create a simple test image with text
    img = Image.new("RGB", (512, 512), color="lightblue")

    # Convert to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    image_bytes = img_bytes.getvalue()

    # Encode to base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return TextToImageResponse(image_base64=image_base64)
