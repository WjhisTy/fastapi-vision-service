"""测试服务模式选择。"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_current_mode_endpoints() -> None:
    """测试当前模式是否暴露了正确的端点。"""
    from app.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        if settings.service_mode == "t2i":
            response = await client.get("/t2i/generate")
            assert response.status_code in [
                405,
                422,
            ]  # GET 方法不允许，但端点存在

            response = await client.get("/vl/understand")
            assert response.status_code == 404  # vl 端点不存在

        elif settings.service_mode == "vl":
            response = await client.get("/vl/understand")
            assert response.status_code in [
                405,
                422,
            ]  # GET 方法不允许，但端点存在

            response = await client.get("/t2i/generate")
            assert response.status_code == 404  # t2i 端点不存在
