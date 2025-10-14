"""文生图 API 路由（HTTP 和 WebSocket）。"""

import base64
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from pydantic import BaseModel

from app.models.t2i_hunyuan import HunyuanDiTModel
from app.queue import run_exclusive

router = APIRouter(prefix="/t2i", tags=["text-to-image"])

# 全局变量类型标注
_model: HunyuanDiTModel | None = None


def get_model() -> HunyuanDiTModel | None:
    """获取或初始化文生图模型（单例模式）。"""
    from app.config import settings

    if settings.demo_mode:
        return None

    global _model
    if _model is None:
        _model = HunyuanDiTModel()
    return _model


class TextToImageRequest(BaseModel):
    """文生图请求模式。"""

    prompt: str


class TextToImageResponse(BaseModel):
    """文生图响应模式。"""

    image_base64: str


@router.post("/generate", response_model=TextToImageResponse)
async def generate_image_http(request: TextToImageRequest) -> TextToImageResponse:
    """
    从文本提示生成图像（HTTP 端点）。

    Args:
        request: 文本提示

    Returns:
        Base64 编码的 PNG 图像
    """
    model = get_model()

    # 独占执行推理（队列管理）
    image_bytes = await run_exclusive(lambda: model.generate_image(request.prompt))

    # 编码为 Base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return TextToImageResponse(image_base64=image_base64)


@router.post("/generate/image", response_class=Response)
async def generate_image_binary(request: TextToImageRequest) -> Response:
    """
    从文本提示生成图像，返回原始 PNG 字节。

    Args:
        request: 文本提示

    Returns:
        PNG 图像字节
    """
    model = get_model()

    # 独占执行推理
    image_bytes = await run_exclusive(lambda: model.generate_image(request.prompt))

    return Response(content=image_bytes, media_type="image/png")


@router.websocket("/ws")
async def generate_image_websocket(websocket: WebSocket) -> None:
    """
    文生图 WebSocket 端点。

    协议：
        客户端发送: {"prompt": "a beautiful sunset"}
        服务器响应: {"image_base64": "iVBORw0KGgo..."}
    """
    await websocket.accept()
    model = get_model()

    try:
        while True:
            # 接收请求
            data: dict[str, Any] = await websocket.receive_json()
            prompt = data.get("prompt", "")

            if not prompt:
                await websocket.send_json({"error": "Missing prompt"})
                continue

            # 生成图像
            image_bytes = await run_exclusive(lambda: model.generate_image(prompt))

            # 发送响应
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            await websocket.send_json({"image_base64": image_base64})

    except WebSocketDisconnect:
        print("[T2I WebSocket] Client disconnected")
