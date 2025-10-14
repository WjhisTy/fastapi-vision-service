"""应用程序配置，使用 pydantic-settings。"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量加载的应用程序设置。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 服务模式：可选 "t2i"（文生图）或 "vl"（图片理解）
    service_mode: Literal["t2i", "vl"] = "t2i"

    # 设备配置
    device: Literal["cpu", "cuda"] = "cpu"

    # Hugging Face 缓存目录
    hf_cache_dir: str | None = None

    # 模型路径（可覆盖默认的 HuggingFace 模型 ID）
    t2i_model_id: str = "Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers"
    vl_model_id: str = "Qwen/Qwen2-VL-2B-Instruct"

    t2i_num_inference_steps: int = 10  # CPU推理太慢，先用10步测试
    t2i_guidance_scale: float = 7.5
    t2i_height: int = 768  # HunyuanDiT最小尺寸，不能再小了
    t2i_width: int = 1024

    vl_max_new_tokens: int = 256

    # 服务器设置
    host: str = "0.0.0.0"
    port: int = 8000

    # 演示模式（跳过加载真实模型，用于测试）
    demo_mode: bool = False


settings = Settings()
