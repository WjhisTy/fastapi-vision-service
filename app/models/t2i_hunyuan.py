"""HunyuanDiT 文生图模型"""

import io
from typing import Any

import torch
from diffusers import DiffusionPipeline
from PIL import Image

from app.config import settings


class HunyuanDiTModel:
    """HunyuanDiT 模型封装"""

    def __init__(self) -> None:
        self.device = settings.device
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

        print(f"Loading HunyuanDiT model from {settings.t2i_model_id}...")
        self.pipe = DiffusionPipeline.from_pretrained(
            settings.t2i_model_id,
            torch_dtype=self.dtype,
            cache_dir=settings.hf_cache_dir,
            low_cpu_mem_usage=False,
        )
        self.pipe = self.pipe.to(self.device)
        print("HunyuanDiT model loaded successfully!")

    def generate_image(self, prompt: str) -> bytes:
        """根据文本生成图像"""
        print(f"[T2I] Processing prompt: {prompt}")

        with torch.no_grad():
            result = self.pipe(
                prompt=prompt,
                num_inference_steps=settings.t2i_num_inference_steps,
                guidance_scale=settings.t2i_guidance_scale,
                height=settings.t2i_height,
                width=settings.t2i_width,
            )

        img = result.images[0]

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        print("[T2I] Image generated successfully!")
        return buf.read()

    def _manual_generation_example(self, prompt: str) -> Any:
        """手动生成示例"""
        # 分词
        txt_input = self.pipe.tokenizer(
            [prompt],
            padding="max_length",
            max_length=self.pipe.tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt",
        )
        ids = txt_input.input_ids.to(self.device)

        # 编码
        with torch.no_grad():
            embed = self.pipe.text_encoder(ids)[0]

        # 初始化噪声
        h, w = settings.t2i_height, settings.t2i_width
        channels = self.pipe.unet.config.in_channels
        latents = torch.randn(
            (1, channels, h // 8, w // 8),
            device=self.device,
            dtype=self.dtype,
        )

        # 设置调度器
        self.pipe.scheduler.set_timesteps(settings.t2i_num_inference_steps)
        latents = latents * self.pipe.scheduler.init_noise_sigma

        # 去噪
        for t in self.pipe.scheduler.timesteps:
            with torch.no_grad():
                noise = self.pipe.unet(
                    latents, t, encoder_hidden_states=embed
                ).sample
            latents = self.pipe.scheduler.step(noise, t, latents).prev_sample

        # 解码
        with torch.no_grad():
            img_tensor = self.pipe.vae.decode(
                latents / self.pipe.vae.config.scaling_factor
            ).sample

        # 后处理
        img_tensor = (img_tensor / 2 + 0.5).clamp(0, 1)
        img_data = img_tensor.cpu().permute(0, 2, 3, 1).numpy()[0]
        img_data = (img_data * 255).round().astype("uint8")

        return Image.fromarray(img_data)


