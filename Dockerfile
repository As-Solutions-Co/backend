# Usar imagen base más ligera
FROM ghcr.io/astral-sh/uv:trixie-slim

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

COPY . .


EXPOSE 3000

# Comando optimizado para producción
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "3000", "--workers", "1"]