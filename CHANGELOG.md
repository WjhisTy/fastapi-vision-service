# 更新日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2025-10-10

### ✨ 新增

- 🎨 **文生图服务**: 基于 HunyuanDiT 1.5B 模型
  - HTTP REST API (`/t2i/generate`, `/t2i/generate/image`)
  - WebSocket 实时生成 (`/t2i/ws`)
  - 手动预处理流程展示

- 👁️ **图片理解服务**: 基于 Qwen2.5-VL 3B 模型
  - HTTP REST API (`/vl/understand`, `/vl/understand/upload`)
  - WebSocket 实时问答 (`/vl/ws`)
  - 多模态数据处理演示

- 🔄 **请求队列管理**
  - 使用 `asyncio.Semaphore` 实现
  - 防止并发推理资源冲突
  - 自动排队处理

- ⚙️ **灵活配置系统**
  - 基于 `pydantic-settings`
  - 支持环境变量
  - 单模式运行（t2i/vl 二选一）

- 🐳 **Docker 支持**
  - 完整的 Dockerfile
  - Docker Compose 配置
  - 模型缓存卷挂载
  - CPU/GPU 模式支持

- 🧪 **测试框架**
  - pytest + pytest-asyncio
  - 健康检查测试
  - 模式切换测试
  - 性能测试（可选）

- 🔧 **开发工具链**
  - UV 包管理
  - Ruff 代码格式化和检查
  - Pre-commit hooks
  - GitHub Actions CI

- 📚 **完整文档**
  - README.md - 项目总览
  - QUICKSTART.md - 快速开始
  - DEVELOPMENT.md - 开发指南
  - CONTRIBUTING.md - 贡献指南
  - START_HERE.md - 新手入口
  - 项目完成报告.md - 项目总结

### 🛠️ 技术实现

- 完整的 Python 类型标注
- 全异步 (async/await) 架构
- FastAPI 框架
- PyTorch + Transformers + Diffusers
- 手动 processor 调用演示

### 📋 配置

- Python 3.10+
- 69 个依赖包
- MIT 许可证

### 🔐 安全

- 输入验证（Pydantic）
- CORS 中间件配置
- 环境变量隔离

### 📦 部署

- 支持本地运行
- Docker 容器化
- Docker Compose 编排
- 跨平台支持（Windows/Linux/macOS/WSL2）

### 📝 文档

- 7 个主要文档文件
- 详细的 API 文档（Swagger UI）
- 代码注释完整
- 示例客户端代码

---

## [未来计划]

### 🚀 即将推出

- [ ] 批处理支持
- [ ] 流式输出
- [ ] 结果缓存
- [ ] 更多模型支持

### 💡 考虑中

- [ ] xDiT 包装（文生图加速）
- [ ] vLLM 包装（VL 加速）
- [ ] 性能监控（Prometheus）
- [ ] Web UI 界面
- [ ] 模型热更新

---

## 版本说明

### 版本号格式：主版本.次版本.修订号

- **主版本**：不兼容的 API 变更
- **次版本**：向下兼容的功能新增
- **修订号**：向下兼容的问题修复

### 变更类型

- **新增** - 新功能
- **修改** - 现有功能的变更
- **弃用** - 即将删除的功能
- **移除** - 已删除的功能
- **修复** - Bug 修复
- **安全** - 安全相关修复

[0.1.0]: https://github.com/yourusername/fastapi-vision-service/releases/tag/v0.1.0

