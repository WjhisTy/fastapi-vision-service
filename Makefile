.PHONY: help install dev test lint format clean docker-build docker-run-t2i docker-run-vl

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev           - Install dev dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linter"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean cache files"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run-t2i - Run T2I service in Docker"
	@echo "  make docker-run-vl  - Run VL service in Docker"

install:
	uv sync

dev:
	uv sync --extra dev

test:
	uv run pytest -v

lint:
	uv run ruff check

format:
	uv run ruff format
	uv run ruff check --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t fastapi-vision-service .

docker-run-t2i:
	docker run -d -p 8000:8000 \
		-e SERVICE_MODE=t2i \
		-e DEVICE=cpu \
		-v $(PWD)/hf_cache:/models/hf \
		fastapi-vision-service

docker-run-vl:
	docker run -d -p 8000:8000 \
		-e SERVICE_MODE=vl \
		-e DEVICE=cpu \
		-v $(PWD)/hf_cache:/models/hf \
		fastapi-vision-service

run-t2i:
	SERVICE_MODE=t2i uv run uvicorn app.main:app --reload

run-vl:
	SERVICE_MODE=vl uv run uvicorn app.main:app --reload

