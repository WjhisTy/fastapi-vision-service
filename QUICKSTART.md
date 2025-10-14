# 快速开始指南

本文档帮助你快速上手 FastAPI Vision Service 项目。

## 🎯 第一次使用

### 1. 确保环境准备好

```bash
# 检查 Python 版本（需要 3.10+）
python --version

# 检查 UV 是否安装
uv --version

# 如果没有 UV，安装它
pip install uv
```

### 2. 克隆并进入项目

```bash
cd D:\aaaaa\fastapi-vision-service
```

### 3. 安装依赖

```bash
uv sync --extra dev
```

这会安装所有需要的包，包括开发工具。

## 🚀 运行服务

### 方式一：本地直接运行（推荐初学者）

#### 运行文生图服务

```bash
# Windows PowerShell
$env:SERVICE_MODE="t2i"
uv run uvicorn app.main:app --reload

# Linux/macOS
SERVICE_MODE=t2i uv run uvicorn app.main:app --reload
```

#### 运行图片理解服务

```bash
# Windows PowerShell
$env:SERVICE_MODE="vl"
uv run uvicorn app.main:app --reload

# Linux/macOS
SERVICE_MODE=vl uv run uvicorn app.main:app --reload
```

### 方式二：使用 Docker

#### 先构建镜像

```bash
docker build -t fastapi-vision-service .
```

#### 运行文生图服务

```bash
# Windows PowerShell
docker run -p 8000:8000 `
  -e SERVICE_MODE=t2i `
  -e DEVICE=cpu `
  -v ${PWD}/hf_cache:/models/hf `
  fastapi-vision-service

# Linux/macOS/WSL2
docker run -p 8000:8000 \
  -e SERVICE_MODE=t2i \
  -e DEVICE=cpu \
  -v $(pwd)/hf_cache:/models/hf \
  fastapi-vision-service
```

#### 运行图片理解服务

```bash
# Windows PowerShell
docker run -p 8000:8000 `
  -e SERVICE_MODE=vl `
  -e DEVICE=cpu `
  -v ${PWD}/hf_cache:/models/hf `
  fastapi-vision-service

# Linux/macOS/WSL2
docker run -p 8000:8000 \
  -e SERVICE_MODE=vl \
  -e DEVICE=cpu \
  -v $(pwd)/hf_cache:/models/hf \
  fastapi-vision-service
```

#### 使用 Docker Compose（最简单）

```bash
# 启动文生图服务
docker-compose --profile t2i up

# 启动图片理解服务
docker-compose --profile vl up

# 后台运行
docker-compose --profile t2i up -d
```

## 📖 测试 API

### 1. 打开浏览器查看 API 文档

服务启动后，访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. 测试健康检查

```bash
curl http://localhost:8000/health
```

### 3. 测试文生图（如果运行 t2i 模式）

```bash
# 生成图片（返回 Base64）
curl -X POST "http://localhost:8000/t2i/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset"}'

# 生成图片（返回 PNG 文件）
curl -X POST "http://localhost:8000/t2i/generate/image" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cute cat"}' \
  --output cat.png
```

### 4. 测试图片理解（如果运行 vl 模式）

需要先准备一张测试图片 `test.jpg`：

```bash
# 上传图片并提问
curl -X POST "http://localhost:8000/vl/understand/upload" \
  -F "image=@test.jpg" \
  -F "question=What is in this image?"
```

### 5. 使用 Python 客户端测试

项目包含了一个测试脚本 `examples_client.py`：

```bash
uv run python examples_client.py
```

## 🧪 运行测试

```bash
# 运行所有测试
uv run pytest -v

# 运行特定测试
uv run pytest tests/test_health.py -v

# 查看测试覆盖率
uv run pytest --cov=app --cov-report=html
```

## 🛠️ 开发工作流

### 1. 格式化代码

```bash
uv run ruff format
```

### 2. 检查代码质量

```bash
uv run ruff check

# 自动修复问题
uv run ruff check --fix
```

### 3. 运行 pre-commit hooks

```bash
# 手动运行所有 hooks
uv run pre-commit run --all-files
```

## 📝 常见问题

### Q: 首次运行很慢？

A: 第一次运行会下载模型（数 GB），请耐心等待。模型会缓存到 `hf_cache/` 目录。

### Q: 内存不足怎么办？

A: 这些模型比较大。文生图模型约需 6GB RAM，图片理解模型约需 8GB RAM。建议：
- 使用 CPU 模式（更省内存）
- 一次只运行一个服务
- 考虑使用更小的模型

### Q: 如何切换到 GPU？

A: 设置环境变量：

```bash
# 本地运行
export DEVICE=cuda  # Linux/macOS
$env:DEVICE="cuda"  # Windows

# Docker 运行
docker run --gpus all -e DEVICE=cuda ...
```

### Q: 如何更换模型？

A: 修改环境变量：

```bash
export T2I_MODEL_ID="your/model-id"
export VL_MODEL_ID="your/model-id"
```

### Q: WebSocket 怎么用？

A: 可以使用浏览器 JavaScript：

```javascript
// 文生图
const ws = new WebSocket('ws://localhost:8000/t2i/ws');
ws.onopen = () => ws.send(JSON.stringify({prompt: "a dog"}));
ws.onmessage = (e) => console.log(JSON.parse(e.data));

// 图片理解
const ws = new WebSocket('ws://localhost:8000/vl/ws');
ws.onopen = () => ws.send(JSON.stringify({
  image_base64: "...",
  question: "what is this?"
}));
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

## 🎓 下一步学习

1. 阅读完整的 [README.md](README.md)
2. 查看 [API 文档](http://localhost:8000/docs)
3. 研究源代码：
   - `app/main.py` - 入口
   - `app/models/` - 模型实现
   - `app/routers/` - API 路由
4. 尝试修改配置参数
5. 自己写新的测试用例

## 💡 提示

- 使用 `--reload` 参数时，代码修改会自动重载
- 查看日志了解模型加载和推理过程
- 第一次生成可能较慢，之后会快很多
- 使用 `hf_cache` 目录挂载避免重复下载模型

祝你使用愉快！ 🚀

