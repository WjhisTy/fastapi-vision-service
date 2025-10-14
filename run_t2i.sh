#!/bin/bash
echo "Starting Text-to-Image Service..."
export SERVICE_MODE=t2i
export DEVICE=cpu
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

