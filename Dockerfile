# source: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers

ARG PYTHON_VERSION=3.13


# ======== Install API dependencies using uv ========
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
FROM python:${PYTHON_VERSION} AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable --no-dev  --compile-bytecode

COPY . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --no-dev --compile-bytecode


# ======== Build the base image ========
FROM python:${PYTHON_VERSION}-slim AS base

WORKDIR /app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup --uid 1000 appuser

COPY --from=builder --chown=app:app \
    /app/.venv /app/.venv

COPY \
    logging.prod.yaml \
    ./

ENV LOGS_CONFIG_PATH=/app/logging.prod.yaml
ENV ENVIRONMENT=production

RUN chown -R appuser:appgroup /app
USER appuser


# ======= Build the application image ========
FROM base AS app
ENTRYPOINT ["/app/.venv/bin/app"]


# ======= Build the API image ========
FROM base AS api
ENTRYPOINT ["/app/.venv/bin/uvicorn", "api:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
