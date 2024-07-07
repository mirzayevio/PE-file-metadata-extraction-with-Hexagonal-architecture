FROM python:3.11-slim

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIRc

COPY . /app

RUN poetry install --without dev

CMD ["python", "main.py"]
