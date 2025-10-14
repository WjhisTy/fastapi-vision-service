"""FastAPI 应用程序入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title="FastAPI Vision Service",
    description="Text-to-Image and Vision-Language API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
# 联合类型
async def health_check() -> dict[str, str | bool]:
    """健康检查端点。"""
    return {
        "status": "healthy",
        "mode": settings.service_mode,
        "device": settings.device,
    }


if settings.demo_mode:
    from app.routers import t2i_simple

    app.include_router(t2i_simple.router)
    print("Service running in DEMO MODE (no real models)")

elif settings.service_mode == "t2i":
    from app.routers import t2i

    app.include_router(t2i.router)
    print(f"Service running in TEXT-TO-IMAGE mode on {settings.device}")

elif settings.service_mode == "vl":
    from app.routers import vl

    app.include_router(vl.router)
    print(f"Service running in VISION-LANGUAGE mode on {settings.device}")

else:
    raise ValueError(f"Invalid service_mode: {settings.service_mode}")


@app.get("/")
async def root() -> dict[str, str]:
    """根端点，返回服务信息。"""
    return {
        "service": "FastAPI Vision Service",
        "mode": settings.service_mode,
        "version": "0.1.0",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
