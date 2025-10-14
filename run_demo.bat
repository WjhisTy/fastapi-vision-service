@echo off
echo ========================================
echo  FastAPI Vision Service - DEMO MODE
echo  (No real models, instant startup!)
echo ========================================
set SERVICE_MODE=t2i
set DEVICE=cpu
set DEMO_MODE=true
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

