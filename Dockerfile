FROM python:3.12-slim

RUN pip install "poetry==1.8.3"

COPY poetry.lock pyproject.toml /app/
WORKDIR /app
ENV PYTHONPATH="/app"

RUN --mount=type=cache,target=/cache/poetry \
    poetry config virtualenvs.create false && \
    poetry config cache-dir /cache/poetry && \
    poetry install --only main --no-interaction --no-ansi

COPY src /app
COPY tests /app/tests