# Dockerfile.prod

# ---------- Builder ----------
FROM python:3.13-slim-trixie AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.7 /uv /uvx /bin/

WORKDIR /app

ENV UV_PYTHON_DOWNLOADS=0
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

# Install dependencies in a cached layer
COPY pyproject.toml uv.lock .python-version README.md ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-editable

# Copy application source
COPY src ./src

# Install project itself, non-editable
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable


# ---------- Runtime ----------
FROM python:3.13-slim-trixie AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Copy only the prepared virtual environment
COPY --from=builder /app/.venv /app/.venv

EXPOSE 8000

CMD ["uvicorn", "fastapi_learning_project.main:app", "--host", "0.0.0.0", "--port", "8000"]