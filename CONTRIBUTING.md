# 贡献指南

感谢你考虑为 FastAPI Vision Service 做出贡献！

## 🤝 如何贡献

### 报告 Bug

如果你发现了 bug，请：

1. 检查 [Issues](https://github.com/yourusername/fastapi-vision-service/issues) 确认问题未被报告
2. 创建新 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 期望的行为
   - 实际的行为
   - 环境信息（OS、Python 版本等）
   - 相关截图或日志

### 提出新功能

1. 先创建 Issue 讨论功能的必要性
2. 等待维护者反馈
3. 获得批准后开始开发

### 提交代码

#### 1. Fork 项目

```bash
# Fork 到你的账号
# 克隆你的 fork
git clone https://github.com/your-username/fastapi-vision-service.git
cd fastapi-vision-service
```

#### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：
- `feature/xxx` - 新功能
- `fix/xxx` - Bug 修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 代码重构
- `test/xxx` - 测试相关

#### 3. 开发环境设置

```bash
# 安装依赖
uv sync --extra dev

# 安装 pre-commit hooks
uv run pre-commit install
```

#### 4. 编写代码

遵循以下规范：

**代码规范**:
- 使用类型标注
- 遵循 PEP 8（通过 Ruff 自动格式化）
- 添加必要的注释和文档字符串
- 保持函数简洁，单一职责

**示例**:
```python
async def process_image(image_bytes: bytes, question: str) -> str:
    """
    处理图片并回答问题。

    Args:
        image_bytes: 图片的二进制数据
        question: 关于图片的问题

    Returns:
        文本答案
    """
    # 实现代码
    pass
```

#### 5. 运行测试

```bash
# 格式化代码
uv run ruff format

# 检查代码质量
uv run ruff check --fix

# 运行测试
uv run pytest -v

# 检查类型（可选）
# uv run mypy app/
```

#### 6. 提交代码

使用清晰的 commit message：

```bash
git add .
git commit -m "feat: 添加批处理支持"
```

Commit 格式：
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

示例：
```
feat: 添加批处理队列支持

- 实现批处理队列类
- 添加批处理配置项
- 更新文档
```

#### 7. 推送并创建 Pull Request

```bash
git push origin feature/your-feature-name
```

在 GitHub 上创建 Pull Request：
- 清晰的标题
- 详细的描述（做了什么、为什么、如何测试）
- 关联相关 Issue（如 `Fixes #123`）
- 截图或演示（如果适用）

## 📋 代码审查清单

提交 PR 前请确认：

- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] Ruff 检查通过
- [ ] 更新了相关文档
- [ ] Commit message 清晰明确
- [ ] PR 描述详细完整

## 🧪 测试指南

### 编写测试

测试文件放在 `tests/` 目录：

```python
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_your_feature() -> None:
    """测试你的功能。"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/your-endpoint")
        assert response.status_code == 200
```

### 运行测试

```bash
# 运行所有测试
uv run pytest -v

# 运行特定测试
uv run pytest tests/test_your_feature.py -v

# 查看覆盖率
uv run pytest --cov=app --cov-report=html
```

## 📚 文档指南

### 更新文档

如果你的改动影响用户使用，请更新：
- `README.md` - 主要功能变更
- `QUICKSTART.md` - 使用步骤变更
- `DEVELOPMENT.md` - 开发相关变更
- API 文档（docstring）

### 文档规范

- 使用清晰简洁的中文
- 提供代码示例
- 添加截图说明（如果适用）
- 保持格式一致

## 🎨 代码风格

### Python 代码

```python
# 好的示例
async def generate_image(prompt: str) -> bytes:
    """
    从文本生成图片。

    Args:
        prompt: 文本描述

    Returns:
        PNG 图片的二进制数据
    """
    # 清晰的变量名
    image_bytes = await model.generate(prompt)
    return image_bytes


# 避免的写法
async def gen(p):  # 类型标注缺失，变量名不清晰
    return await model.generate(p)
```

### 导入顺序

```python
# 1. 标准库
import asyncio
from typing import Any

# 2. 第三方库
from fastapi import APIRouter
import torch

# 3. 本地导入
from app.config import settings
from app.models.base import BaseModel
```

## 🐛 调试技巧

### 本地调试

```bash
# 启用 debug 模式
uvicorn app.main:app --reload --log-level debug

# 查看详细日志
SERVICE_MODE=t2i python -m app.main
```

### 使用 pdb 调试

```python
import pdb; pdb.set_trace()  # 设置断点
```

## 📞 获取帮助

如果你需要帮助：

1. 查看 [文档](README.md)
2. 搜索 [已有 Issues](https://github.com/yourusername/fastapi-vision-service/issues)
3. 创建新 Issue 提问
4. 在 PR 中 @ 维护者

## 🏆 贡献者

感谢所有贡献者！

<!-- 这里会自动显示贡献者头像 -->

## 📄 许可证

贡献代码即表示你同意代码使用项目的 MIT 许可证。

---

再次感谢你的贡献！🎉

