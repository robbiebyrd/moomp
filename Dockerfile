FROM python:3.12.6

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.4

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi

COPY docker/entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

COPY . /app
ENTRYPOINT "./entrypoint.sh"
