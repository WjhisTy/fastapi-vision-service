"""视觉语言 API 路由（HTTP 和 WebSocket）。"""

import base64
from typing import Any

from fastapi import APIRouter, File, Form, UploadFile, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.models.vl_qwen import QwenVLModel
from app.queue import run_exclusive

router = APIRouter(prefix="/vl", tags=["vision-language"])

_model: QwenVLModel | None = None


def get_model() -> QwenVLModel:
    """获取或初始化视觉语言模型（单例模式）。"""
    global _model
    if _model is None:
        _model = QwenVLModel()
    return _model


class VisionLanguageRequest(BaseModel):
    """视觉语言理解请求模式。"""

    image_base64: str
    question: str


class VisionLanguageResponse(BaseModel):
    """视觉语言理解响应模式。"""

    answer: str


@router.post("/understand", response_model=VisionLanguageResponse)
async def understand_image_http(
    request: VisionLanguageRequest,
) -> VisionLanguageResponse:
    """
    理解图像并回答问题（HTTP 端点，JSON 格式）。

    Args:
        request: Base64 编码的图像和问题

    Returns:
        文本答案
    """
    model = get_model()

    # 解码图像
    image_bytes = base64.b64decode(request.image_base64)

    # 独占执行推理
    answer = await run_exclusive(lambda: model.understand_image(image_bytes, request.question))

    return VisionLanguageResponse(answer=answer)


@router.post("/understand/upload", response_model=VisionLanguageResponse)
async def understand_image_upload(
    image: UploadFile = File(...),
    question: str = Form(...),
) -> VisionLanguageResponse:
    """
    理解图像并回答问题（HTTP 端点，文件上传）。

    Args:
        image: 上传的图像文件
        question: 关于图像的问题

    Returns:
        文本答案
    """
    model = get_model()

    # 读取图像字节
    image_bytes = await image.read()

    # 独占执行推理
    answer = await run_exclusive(lambda: model.understand_image(image_bytes, question))

    return VisionLanguageResponse(answer=answer)


@router.websocket("/ws")
async def understand_image_websocket(websocket: WebSocket) -> None:
    """
    视觉语言理解 WebSocket 端点。

    协议：
        客户端发送: {"image_base64": "base64...", "question": "What is this?"}
        服务器响应: {"answer": "This is a cat"}
    """
    await websocket.accept()
    model = get_model()

    try:
        while True:
            # 接收请求
            data: dict[str, Any] = await websocket.receive_json()
            image_base64 = data.get("image_base64", "")
            question = data.get("question", "")

            if not image_base64 or not question:
                await websocket.send_json({"error": "Missing image_base64 or question"})
                continue

            # 解码图像
            image_bytes = base64.b64decode(image_base64)

            # 生成答案
            answer = await run_exclusive(lambda: model.understand_image(image_bytes, question))

            # 发送响应
            await websocket.send_json({"answer": answer})

    except WebSocketDisconnect:
        print("[VL WebSocket] Client disconnected")
