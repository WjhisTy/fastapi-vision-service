# FastAPI Vision Service

一个基于 FastAPI 的视觉服务，支持文生图（Text-to-Image）和图片理解（Vision-Language）两种模式。

## ✨ 特性

- 🎨 **文生图模式**：使用 HunyuanDiT 模型，从文本描述生成图片
- 👁️ **图片理解模式**：使用 Qwen2.5-VL 模型，理解图片内容并回答问题
- 🚀 **双协议支持**：HTTP REST API 和 WebSocket 实时通信
- 🔄 **请求队列管理**：自动排队，避免并发推理导致资源冲突
- 🐳 **Docker 容器化**：一键部署，支持 CPU/GPU
- ✅ **类型安全**：完整的 Python 类型标注
- 🧹 **代码质量**：使用 Ruff 格式化和 Pre-commit hooks
- 🧪 **单元测试**：使用 Pytest 进行测试
- 🔧 **CI/CD**：GitHub Actions 自动化测试和构建

## 📋 技术栈

- **框架**：FastAPI + Uvicorn
- **包管理**：UV (Astral)
- **深度学习**：PyTorch + Transformers + Diffusers
- **模型**：
  - 文生图：Tencent HunyuanDiT 1.5B
  - 图片理解：Qwen2.5-VL 3B
- **容器化**：Docker + Docker Compose
- **代码质量**：Ruff + Pre-commit
- **测试**：Pytest + pytest-asyncio

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Docker (可选，用于容器化部署)
- Git
- UV 包管理器

### 安装 UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
pip install uv
```

### 本地开发

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/fastapi-vision-service.git
cd fastapi-vision-service
```

2. **安装依赖**

```bash
uv sync --extra dev
```

3. **配置环境变量**

复制 `env.example` 到 `.env` 并修改配置：

```bash
cp env.example .env
```

编辑 `.env` 文件设置服务模式：

```env
SERVICE_MODE=t2i  # 或 vl
DEVICE=cpu        # 或 cuda (需要 GPU)
```

4. **运行服务**

```bash
# 直接运行
uv run uvicorn app.main:app --reload

# 或使用 Python
uv run python -m app.main
```

5. **访问 API 文档**

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐳 Docker 部署

### 构建镜像

```bash
docker build -t fastapi-vision-service .
```

### 运行容器

#### 文生图模式 (CPU)

```bash
docker run -d \
  -p 8000:8000 \
  -e SERVICE_MODE=t2i \
  -e DEVICE=cpu \
  -v $(pwd)/hf_cache:/models/hf \
  fastapi-vision-service
```

#### 图片理解模式 (CPU)

```bash
docker run -d \
  -p 8000:8000 \
  -e SERVICE_MODE=vl \
  -e DEVICE=cpu \
  -v $(pwd)/hf_cache:/models/hf \
  fastapi-vision-service
```

#### GPU 支持

```bash
docker run -d \
  --gpus all \
  -p 8000:8000 \
  -e SERVICE_MODE=t2i \
  -e DEVICE=cuda \
  -v $(pwd)/hf_cache:/models/hf \
  fastapi-vision-service
```

### 使用 Docker Compose

```bash
# 启动文生图服务
docker-compose --profile t2i up -d

# 启动图片理解服务
docker-compose --profile vl up -d

# 停止服务
docker-compose down
```

## 📚 API 使用说明

### 文生图模式 (T2I)

#### HTTP 端点

**生成图片 (返回 Base64)**

```bash
curl -X POST "http://localhost:8000/t2i/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset over the ocean"}'
```

**生成图片 (返回 PNG 二进制)**

```bash
curl -X POST "http://localhost:8000/t2i/generate/image" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cute cat"}' \
  --output image.png
```

#### WebSocket 端点

```javascript
const ws = new WebSocket('ws://localhost:8000/t2i/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    prompt: "a futuristic city at night"
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Image Base64:', data.image_base64);
};
```

### 图片理解模式 (VL)

#### HTTP 端点

**理解图片 (JSON)**

```bash
curl -X POST "http://localhost:8000/vl/understand" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "base64_encoded_image_here",
    "question": "What is in this image?"
  }'
```

**理解图片 (文件上传)**

```bash
curl -X POST "http://localhost:8000/vl/understand/upload" \
  -F "image=@/path/to/image.jpg" \
  -F "question=Describe this image"
```

#### WebSocket 端点

```javascript
const ws = new WebSocket('ws://localhost:8000/vl/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    image_base64: "base64_encoded_image",
    question: "What objects are in this image?"
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Answer:', data.answer);
};
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_health.py -v

# 生成覆盖率报告
uv run pytest --cov=app --cov-report=html
```

### Pre-commit Hooks

安装 pre-commit hooks：

```bash
uv run pre-commit install
```

手动运行所有 hooks：

```bash
uv run pre-commit run --all-files
```

## 🛠️ 开发

### 代码格式化

```bash
# 格式化代码
uv run ruff format

# 检查代码
uv run ruff check

# 自动修复
uv run ruff check --fix
```

### 项目结构

```
fastapi-vision-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── queue.py             # 请求队列管理
│   ├── models/
│   │   ├── __init__.py
│   │   ├── t2i_hunyuan.py  # HunyuanDiT 模型
│   │   └── vl_qwen.py      # Qwen2.5-VL 模型
│   └── routers/
│       ├── __init__.py
│       ├── t2i.py          # 文生图路由
│       └── vl.py           # 图片理解路由
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_mode.py
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI
├── pyproject.toml          # UV 项目配置
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # Docker Compose 配置
├── .pre-commit-config.yaml # Pre-commit 配置
└── README.md
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 可选值 |
|--------|------|--------|--------|
| `SERVICE_MODE` | 服务模式 | `t2i` | `t2i`, `vl` |
| `DEVICE` | 计算设备 | `cpu` | `cpu`, `cuda` |
| `HF_CACHE_DIR` | HuggingFace 缓存目录 | `None` | 任意路径 |
| `T2I_MODEL_ID` | 文生图模型 ID | `Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers` | 任意 HF 模型 |
| `VL_MODEL_ID` | 图片理解模型 ID | `Qwen/Qwen2-VL-2B-Instruct` | 任意 HF 模型 |
| `T2I_NUM_INFERENCE_STEPS` | 推理步数 | `30` | 整数 |
| `T2I_GUIDANCE_SCALE` | 引导强度 | `7.5` | 浮点数 |
| `T2I_HEIGHT` | 图片高度 | `512` | 整数 |
| `T2I_WIDTH` | 图片宽度 | `512` | 整数 |
| `VL_MAX_NEW_TOKENS` | 最大生成 token 数 | `256` | 整数 |
| `HOST` | 服务主机 | `0.0.0.0` | IP 地址 |
| `PORT` | 服务端口 | `8000` | 端口号 |

## 📝 模型说明

### 文生图 - HunyuanDiT

- **模型**：Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers
- **类型**：扩散模型 (Diffusion Transformer)
- **输入**：文本描述
- **输出**：512x512 PNG 图像
- **处理流程**：
  1. 文本分词 → input_ids
  2. 文本编码 → text_embeddings
  3. 初始化噪声
  4. 迭代去噪
  5. VAE 解码 → 图像

### 图片理解 - Qwen2.5-VL

- **模型**：Qwen/Qwen2-VL-2B-Instruct
- **类型**：视觉-语言多模态模型
- **输入**：图像 + 文本问题
- **输出**：文本回答
- **处理流程**：
  1. 图像预处理 → pixel_values
  2. 文本分词 → input_ids (含图像 token)
  3. 模型生成 → output_ids
  4. 解码 → 文本

## 🚧 已知限制

- 单次服务启动只支持一种模式（T2I 或 VL）
- 使用队列机制，不支持并发推理
- GPU 模式需要 CUDA 环境
- 首次运行会下载模型（数 GB）

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题，请提交 Issue 或联系维护者。

---

**享受 AI 视觉服务！** 🎉

