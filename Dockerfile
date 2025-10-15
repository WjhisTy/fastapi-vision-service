# 使用 Python 3.10
FROM python:3.10-slim

# 安装系统依赖（包括ML库需要的依赖）
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY pyproject.toml ./
COPY src ./src
COPY app ./app

# 升级pip并安装依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings python-multipart pillow httpx transformers diffusers accelerate safetensors sentencepiece protobuf && \
    pip install --no-cache-dir -e .

# 设置Hugging Face缓存目录
ENV HF_HOME=/models/hf
ENV TRANSFORMERS_CACHE=/models/hf
ENV HF_HUB_CACHE=/models/hf

# 暴露端口
EXPOSE 8000

# 运行应用程序
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


