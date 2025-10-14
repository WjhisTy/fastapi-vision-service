"""Performance and load testing examples (optional)."""

import asyncio
import time

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
@pytest.mark.slow
async def test_concurrent_requests_queue() -> None:
    """
    测试并发请求时的排队机制。

    这个测试验证多个并发请求会被正确排队处理。
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=30.0,
    ) as client:
        # 发送多个并发健康检查请求
        tasks = [client.get("/health") for _ in range(10)]

        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time

        # 验证所有请求都成功
        assert all(r.status_code == 200 for r in responses)

        # 验证响应合理（不会因并发而崩溃）
        print(f"10 concurrent requests completed in {elapsed:.2f}s")


@pytest.mark.asyncio
@pytest.mark.slow
async def test_response_time() -> None:
    """
    测试响应时间（健康检查应该很快）。
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        start_time = time.time()
        response = await client.get("/health")
        elapsed = time.time() - start_time

        assert response.status_code == 200
        assert elapsed < 1.0  # 健康检查应该在1秒内完成
        print(f"Health check response time: {elapsed * 1000:.2f}ms")


# 注意：这些测试默认不运行，需要添加 -m slow 参数
# 运行命令: uv run pytest -v -m slow
