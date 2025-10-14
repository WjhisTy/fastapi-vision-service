@echo off
echo Starting Text-to-Image Service...
set SERVICE_MODE=t2i
set DEVICE=cpu
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

