FROM python:3.14-alpine3.23

RUN apk add --no-cache

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

WORKDIR /app

COPY uv.lock .
COPY pyproject.toml .
RUN uv sync --no-dev

COPY . .

# RUN adduser -D appuser
# USER appuser

CMD [ "uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]