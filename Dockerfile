FROM python:3.12-alpine AS base

FROM base AS builder

ENV UV_COMPILE_BYTECODE=1 LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /build
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project --locked --no-editable

FROM base AS final

WORKDIR /app

COPY --from=builder /build/.venv .venv
COPY ./kitty_bot ./kitty_bot

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "kitty_bot"]