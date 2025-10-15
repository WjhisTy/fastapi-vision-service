# 使用标准Python镜像（不是slim，包含更多预装库）
FROM python:3.10

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

# 升级pip
RUN pip install --no-cache-dir --upgrade pip

# 安装构建工具
RUN pip install --no-cache-dir hatchling

# 安装PyTorch (CPU版本)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 安装基础依赖
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic \
    pydantic-settings \
    python-multipart \
    pillow \
    httpx

# 安装ML库
RUN pip install --no-cache-dir \
    transformers \
    diffusers \
    accelerate \
    safetensors \
    sentencepiece \
    protobuf

# 安装项目
RUN pip install --no-cache-dir -e .

# 设置Hugging Face缓存目录
ENV HF_HOME=/models/hf
ENV TRANSFORMERS_CACHE=/models/hf
ENV HF_HUB_CACHE=/models/hf

# 暴露端口
EXPOSE 8000

# 运行应用程序
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


