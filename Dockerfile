# --- Этап 1: Сборка зависимостей (остается без изменений) ---
FROM python:3.14-alpine3.23 AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/
WORKDIR /app
COPY uv.lock .
COPY pyproject.toml .
RUN uv sync --frozen --no-dev --link-mode=copy

# --- Этап 2: Финальный образ ТОЛЬКО для миграций ---
FROM python:3.14-alpine3.23 AS migrator
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
# Копируем конфигурацию и файлы миграций
COPY --chown=appuser:appgroup alembic.ini ./
COPY --chown=appuser:appgroup alembic ./alembic
# ДОБАВЛЯЕМ КОПИРОВАНИЕ ПАПКИ APP, чтобы env.py мог импортировать модели
COPY --chown=appuser:appgroup ./app ./app

USER appuser
CMD ["sh", "-c", "alembic upgrade head"]


# --- Этап 3: Финальный образ ТОЛЬКО для запуска приложения ---
FROM python:3.14-alpine3.23 AS runner
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --chown=appuser:appgroup ./app ./app

USER appuser
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
