FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install deps before copying app code — layer is cached until pyproject.toml or uv.lock changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD uv run python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

CMD uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
