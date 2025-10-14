# 使用 Python 3.10
FROM python:3.10-slim

# 安装
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY app ./app
COPY src ./src

# 安装依赖
RUN uv sync --no-dev

# 设置Hugging Face缓存目录
ENV HF_HOME=/models/hf
ENV TRANSFORMERS_CACHE=/models/hf
ENV HF_HUB_CACHE=/models/hf

# 暴露端口
EXPOSE 8000

# 运行应用程序
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


