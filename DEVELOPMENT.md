# 开发指南

本文档面向想要深入理解和修改项目的开发者。

## 📚 学习路线（从零开始）

如果你是零基础，建议按以下顺序学习：

### 1. Python 基础（1-2周）
- 变量、数据类型、函数
- 类和面向对象
- 异步编程（async/await）
- 类型标注（Type Hints）
- 推荐资源：
  - [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
  - [廖雪峰 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400)

### 2. FastAPI 框架（3-5天）
- HTTP 协议基础
- REST API 概念
- FastAPI 路由、请求、响应
- WebSocket 通信
- 推荐资源：
  - [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)

### 3. 深度学习基础（1-2周）
- PyTorch 基础
- Transformer 模型原理
- 扩散模型（Diffusion）基础
- 推荐资源：
  - [PyTorch 官方教程](https://pytorch.org/tutorials/)
  - [Hugging Face 课程](https://huggingface.co/course)

### 4. 工具链（2-3天）
- Git 版本控制
- Docker 容器化
- UV 包管理
- 代码质量工具（Ruff, Pre-commit）
- 推荐资源：
  - [Pro Git 中文版](https://git-scm.com/book/zh/v2)
  - [Docker 从入门到实践](https://yeasy.gitbook.io/docker_practice/)

## 🏗️ 项目架构详解

### 核心模块说明

#### 1. `app/config.py` - 配置管理
```python
# 使用 pydantic-settings 从环境变量加载配置
# 支持 .env 文件
# 类型安全的配置访问
```

**关键知识点**：
- Pydantic BaseSettings 的使用
- 环境变量管理
- 配置验证

#### 2. `app/queue.py` - 请求队列
```python
# 使用 asyncio.Semaphore 控制并发
# 确保同时只有一个推理请求执行
```

**关键知识点**：
- asyncio 并发控制
- Semaphore 信号量机制
- 为什么需要排队（避免显存 OOM）

#### 3. `app/models/t2i_hunyuan.py` - 文生图模型
```python
# HunyuanDiT 扩散模型实现
# 展示手动预处理流程：
# 1. 文本分词 tokenization
# 2. 文本编码 text encoding
# 3. 噪声初始化
# 4. 迭代去噪
# 5. VAE 解码
```

**关键知识点**：
- Diffusion Pipeline 的内部工作原理
- Tokenizer 的作用
- Text Encoder（CLIP/T5）
- U-Net/DiT 去噪网络
- VAE（变分自编码器）
- Scheduler（调度器）的作用

**数据流**：
```
文本 → Tokenizer → input_ids (整数张量)
       ↓
   Text Encoder → text_embeddings (浮点张量)
       ↓
   初始噪声 latent (高斯分布)
       ↓
   循环: UNet预测噪声 → Scheduler更新latent
       ↓
   VAE Decoder → 像素图像 (H×W×3)
```

#### 4. `app/models/vl_qwen.py` - 图片理解模型
```python
# Qwen2.5-VL 多模态模型
# 展示手动预处理：
# 1. 图像预处理（resize, normalize）
# 2. 文本分词（含图像占位 token）
# 3. 模型生成
# 4. token 解码
```

**关键知识点**：
- Vision-Language 模型架构
- AutoProcessor 的作用
- 图像 patch 化
- 多模态融合
- 生成式解码

**数据流**：
```
图像 → Processor → pixel_values (归一化张量)
文本 → Processor → input_ids + attention_mask
                   (包含 <image> 特殊 token)
       ↓
   Model.generate() → output_ids (生成的 token)
       ↓
   Decoder → 文本答案
```

#### 5. `app/routers/` - API 路由
- **t2i.py**: 文生图的 HTTP 和 WebSocket 接口
- **vl.py**: 图片理解的 HTTP 和 WebSocket 接口

**关键知识点**：
- FastAPI 路由装饰器
- Pydantic 数据模型
- WebSocket 双向通信
- 异步请求处理
- Base64 编码/解码
- 文件上传处理

#### 6. `app/main.py` - 应用入口
```python
# 根据 SERVICE_MODE 条件导入路由
# 只暴露一种服务接口
```

**关键知识点**：
- FastAPI 应用初始化
- 中间件（CORS）
- 条件路由加载
- 动态模块导入

## 🔬 深入理解关键概念

### 1. 为什么要手动调用 Processor？

**教育目的**：让你理解数据预处理的每一步。

在实际项目中，你可以直接用：
```python
# 简单方式
output = pipe(prompt="a cat")

# vs 手动方式（教学用）
inputs = tokenizer(prompt)
embeddings = text_encoder(inputs.input_ids)
# ... 更多步骤
```

手动方式帮助你理解：
- 输入数据的形状和类型
- 每个组件的作用
- 如何调试和优化

### 2. 为什么禁止并发？

**原因**：
- GPU 显存有限，并发会导致 OOM（内存溢出）
- 模型推理不是线程安全的
- 批处理更高效（可选进阶）

**解决方案**：
```python
# 使用 Semaphore(1) 确保串行执行
async with _inference_semaphore:
    result = await model.generate(...)
```

**进阶**：改为批处理队列，收集多个请求一起推理。

### 3. 为什么只支持一种模式？

**原因**：
- 两个模型同时加载会占用大量内存
- 简化部署和配置
- 明确服务职责

**如何切换**：
- 本地开发：修改环境变量 `SERVICE_MODE`
- Docker：启动不同容器
- 生产环境：部署多个实例

## 🛠️ 开发任务

### 如何添加新模型？

1. 在 `app/models/` 创建新文件，如 `new_model.py`
2. 实现模型类：
```python
class NewModel:
    def __init__(self):
        # 加载模型
        pass
    
    def inference(self, input_data):
        # 推理逻辑
        pass
```

3. 在 `app/routers/` 创建路由
4. 在 `app/main.py` 添加模式分支
5. 更新配置和文档

### 如何优化性能？

#### 1. 使用 torch.compile（PyTorch 2.0+）
```python
self.model = torch.compile(self.model)
```

#### 2. 使用 FP16/BF16
```python
torch_dtype=torch.float16  # 或 bfloat16
```

#### 3. 批处理
将队列改为收集多个请求：
```python
async def batch_process():
    batch = await queue.get_batch(max_size=4)
    results = model.generate_batch(batch)
    return results
```

#### 4. 模型量化
```python
from transformers import BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModel.from_pretrained(..., quantization_config=quantization_config)
```

#### 5. 使用 vLLM 或 xDiT
- vLLM: 优化的推理引擎（VL 模型）
- xDiT: 分布式扩散模型推理（文生图）

### 如何添加性能分析？

使用 torch.profiler：
```python
from torch.profiler import profile, ProfilerActivity

with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    output = model.generate(...)

print(prof.key_averages().table())
prof.export_chrome_trace("trace.json")
```

在浏览器打开 `chrome://tracing` 加载 trace.json 分析。

## 🧪 测试策略

### 单元测试
- 测试配置加载
- 测试路由逻辑
- Mock 模型避免加载大模型

### 集成测试
- 测试完整推理流程
- 需要真实模型（慢）

### 性能测试
```bash
# 使用 locust 或 ab
ab -n 100 -c 10 http://localhost:8000/health
```

## 📦 部署最佳实践

### 1. 生产环境建议
- 使用 GPU 加速
- 设置合理的超时
- 添加日志监控
- 使用负载均衡（多实例）
- 配置健康检查

### 2. 环境变量管理
```bash
# 开发环境
.env

# 生产环境
Kubernetes ConfigMap/Secret
或 Docker Compose env_file
```

### 3. 模型缓存策略
- 预先下载模型到镜像
- 或使用持久化卷挂载

### 4. 监控指标
- 请求延迟
- 队列长度
- GPU 使用率
- 内存使用

## 🔧 故障排查

### 常见问题

#### 1. 模型加载失败
```
原因：网络问题，HF 访问受限
解决：使用镜像站或离线模型
```

#### 2. CUDA Out of Memory
```
原因：模型太大或批次过大
解决：减小batch size，使用FP16，模型量化
```

#### 3. WebSocket 断开
```
原因：推理时间过长
解决：增加超时，添加心跳
```

#### 4. 依赖冲突
```
原因：包版本不兼容
解决：锁定版本，使用 uv.lock
```

## 📚 扩展阅读

### 模型相关
- [Diffusion Models 论文](https://arxiv.org/abs/2006.11239)
- [Vision Transformer](https://arxiv.org/abs/2010.11929)
- [LLaVA 论文](https://arxiv.org/abs/2304.08485)

### 框架相关
- [FastAPI 高级特性](https://fastapi.tiangolo.com/advanced/)
- [Uvicorn 部署](https://www.uvicorn.org/deployment/)
- [Docker 多阶段构建](https://docs.docker.com/develop/develop-images/multistage-build/)

### 优化相关
- [PyTorch Performance Tuning](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
- [HuggingFace Optimization](https://huggingface.co/docs/transformers/performance)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 `git checkout -b feature/xxx`
3. 提交代码 `git commit -m 'Add xxx'`
4. 推送分支 `git push origin feature/xxx`
5. 创建 Pull Request

### 代码规范
- 遵循 PEP 8
- 使用类型标注
- 添加文档字符串
- 通过 Ruff 检查
- 编写测试用例

### Commit 规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

祝你开发愉快！有问题欢迎提 Issue！ 🚀

