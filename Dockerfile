# ---------- Builder ----------
FROM python:3.13-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.7 /uv /uvx /bin/

WORKDIR /app

ENV UV_PYTHON_DOWNLOADS=0 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# Install dependencies in a cached layer
COPY pyproject.toml uv.lock .python-version README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

# Copy application source
COPY src ./src

# Install project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# ---------- Runtime ----------
FROM python:3.13-slim-trixie AS runtime

WORKDIR /app

# Security: Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy venv and source code from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --chown=appuser:appuser src ./src

# Switch to non-root user
USER appuser

EXPOSE 8000

# Use FastAPI CLI's production mode for automatic worker management
CMD ["fastapi", "run", "src/fastapi_learning_project/main.py", "--host", "0.0.0.0", "--port", "8000"]