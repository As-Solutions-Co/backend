FROM ghcr.io/astral-sh/uv:trixie-slim
WORKDIR /app
COPY . .
RUN uv sync --locked
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "3000"]
