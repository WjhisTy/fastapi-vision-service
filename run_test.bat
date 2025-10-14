@echo off
echo Starting Test Mode (No Heavy Models)...
set SERVICE_MODE=t2i
set DEVICE=cpu
set TEST_MODE=1
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

