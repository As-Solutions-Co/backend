FROM ghcr.io/astral-sh/uv:trixie-slim
WORKDIR /app
COPY . .
RUN uv sync --locked
EXPOSE 3000
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "3000"]
