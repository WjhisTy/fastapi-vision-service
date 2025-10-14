@echo off
echo Starting Vision-Language Service...
set SERVICE_MODE=vl
set DEVICE=cpu
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

