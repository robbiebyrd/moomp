FROM python:3.12.6

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install
RUN ls -lart

COPY . .

ENTRYPOINT ["poetry", "run", "python", "-m", "main", "telnet", "Hereville"]
