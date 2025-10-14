"""Qwen2.5-VL 视觉语言模型实现，包含手动预处理步骤。"""

import io
from typing import Any

import torch
from PIL import Image
from transformers import AutoModelForVision2Seq, AutoProcessor

from app.config import settings


class QwenVLModel:
    """
    Qwen2.5-VL 视觉语言模型封装。

    此实现展示了手动预处理步骤：
    1. 图像预处理 -> pixel_values
    2. 文本分词 -> input_ids
    3. 模型生成
    4. Token 解码 -> 文本
    """

    def __init__(self) -> None:
        """初始化 Qwen2.5-VL 模型。"""
        self.device = settings.device
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

        print(f"Loading Qwen2.5-VL model from {settings.vl_model_id}...")

        # 加载 processor 和模型
        self.processor = AutoProcessor.from_pretrained(
            settings.vl_model_id,
            cache_dir=settings.hf_cache_dir,
        )

        self.model = AutoModelForVision2Seq.from_pretrained(
            settings.vl_model_id,
            torch_dtype=self.dtype,
            cache_dir=settings.hf_cache_dir,
        )
        self.model = self.model.to(self.device)
        self.model.eval()

        print("Qwen2.5-VL model loaded successfully!")

    def understand_image(self, image_bytes: bytes, question: str) -> str:
        """
        理解图像并回答问题。

        处理流程（手动预处理演示）：
        1. 从字节加载图像
        2. Processor 处理：
           - 图像调整大小/归一化 -> pixel_values
           - 文本分词 -> input_ids
           - 插入图像 tokens
        3. 模型生成 tokens
        4. 解码 tokens -> 文本答案

        Args:
            image_bytes: 图像文件字节
            question: 关于图像的问题

        Returns:
            描述图像的文本答案
        """
        print(f"[VL] Processing question: {question}")

        # 加载图像
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        # FIXME: 需要添加图像大小检查，太大的图片可能导致OOM

        # 步骤 2: 处理输入（手动预处理演示）
        # Processor 的作用：
        # - 图像: 调整大小、归一化、转换为张量 -> pixel_values
        # - 文本: 分词、添加特殊 tokens -> input_ids
        inputs = self.processor(
            images=image,
            text=question,
            return_tensors="pt",
        )

        # 移动到设备
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        print(f"[VL] Input shapes: {[(k, v.shape) for k, v in inputs.items()]}")

        # 步骤 3: 生成响应
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=settings.vl_max_new_tokens,
                do_sample=False,
            )

        # 步骤 4: 将 tokens 解码为文本
        # 跳过特殊 tokens 以获得干净的输出
        answer = self.processor.batch_decode(output_ids, skip_special_tokens=True)[0]

        print(f"[VL] Generated answer: {answer}")
        return answer

    def _manual_preprocessing_example(self, image_bytes: bytes, question: str) -> dict[str, Any]:
        """
        手动预处理步骤示例（用于教学目的）。

        展示 processor 内部的操作：
        1. 图像预处理
        2. 文本分词
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        inputs = self.processor(
            images=image,
            text=question,
            return_tensors="pt",
        )

        return inputs
