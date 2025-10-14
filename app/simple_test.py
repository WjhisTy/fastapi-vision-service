"""Minimal FastAPI test - no dependencies."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Simple root endpoint."""
    return {"status": "ok", "message": "Service is working!"}


@app.get("/health")
async def health():
    """Simple health check."""
    return {"status": "healthy"}


@app.get("/test")
async def test():
    """Test endpoint."""
    return {"test": "This is a simple test response"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
