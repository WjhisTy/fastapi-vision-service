#!/bin/bash
echo "Starting Vision-Language Service..."
export SERVICE_MODE=vl
export DEVICE=cpu
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

