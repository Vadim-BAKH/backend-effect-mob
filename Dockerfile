FROM python:3.12.3-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
pip install --no-cache-dir "poetry==2.1.3" -i https://pypi.org/simple && \
poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY fastapi_app/ /app/fastapi_app

EXPOSE 8000

ENV PYTHONPATH=/app
