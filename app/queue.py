"""请求队列管理，防止模型并发推理。"""

import asyncio
from collections.abc import Callable
from typing import TypeVar

# 定义泛型类型变量
T = TypeVar("T")

# 用信号量限制并发，避免多个请求同时推理导致爆显存
# NOTE: 这里设为1是因为单卡推理，如果是多卡可以调大
_inference_semaphore = asyncio.Semaphore(1)


async def run_exclusive(func: Callable[[], T]) -> T:
    """
    在线程池中独占执行同步函数（不允许并发执行）。

    这确保模型推理请求一次只处理一个，
    防止 GPU/CPU 资源冲突和内存溢出问题。

    Args:
        func: 要执行的同步函数

    Returns:
        函数的返回结果
    """
    async with _inference_semaphore:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func)
