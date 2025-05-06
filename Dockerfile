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


# ======== Build the application image ========
FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

COPY --from=builder --chown=app:app \
    /app/.venv /app/.venv

COPY \
    logging.prod.yaml \
    ./

ENV LOG_CONFIG_PATH=/app/logging.prod.yaml
ENV ENVIRONMENT=production

CMD ["/app/.venv/bin/app"]