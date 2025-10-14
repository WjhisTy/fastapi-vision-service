"""Example client scripts for testing the API."""

import asyncio
import base64
from pathlib import Path

import httpx


async def test_t2i_http() -> None:
    """Test Text-to-Image HTTP endpoint."""
    print("Testing T2I HTTP endpoint...")

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/t2i/generate",
            json={"prompt": "a beautiful sunset over the ocean"},
            timeout=60.0,
        )

        if response.status_code == 200:
            data = response.json()
            image_base64 = data["image_base64"]

            # Save image
            image_bytes = base64.b64decode(image_base64)
            Path("output_t2i.png").write_bytes(image_bytes)
            print("✅ Image saved to output_t2i.png")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


async def test_vl_http() -> None:
    """Test Vision-Language HTTP endpoint."""
    print("Testing VL HTTP endpoint...")

    # You need to provide a test image
    test_image_path = "test_image.jpg"

    if not Path(test_image_path).exists():
        print(f"❌ Test image {test_image_path} not found")
        return

    # Read and encode image
    image_bytes = Path(test_image_path).read_bytes()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/vl/understand",
            json={
                "image_base64": image_base64,
                "question": "What is in this image?",
            },
            timeout=60.0,
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Answer: {data['answer']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


async def test_vl_upload() -> None:
    """Test Vision-Language upload endpoint."""
    print("Testing VL upload endpoint...")

    test_image_path = "test_image.jpg"

    if not Path(test_image_path).exists():
        print(f"❌ Test image {test_image_path} not found")
        return

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        files = {"image": open(test_image_path, "rb")}
        data = {"question": "Describe this image in detail"}

        response = await client.post(
            "/vl/understand/upload",
            files=files,
            data=data,
            timeout=60.0,
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Answer: {result['answer']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")


async def main() -> None:
    """Run example tests based on service mode."""
    # Check service mode
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/health")
        if response.status_code == 200:
            health = response.json()
            mode = health.get("mode")
            print(f"Service mode: {mode}")

            if mode == "t2i":
                await test_t2i_http()
            elif mode == "vl":
                await test_vl_http()
                # await test_vl_upload()
        else:
            print("❌ Service not available")


if __name__ == "__main__":
    asyncio.run(main())
