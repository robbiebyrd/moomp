FROM python:3.12-bookworm

COPY . .

RUN rm -rf .venv .run

RUN pip install poetry

RUN poetry install

RUN chmod +x docker/entrypoint.sh

CMD ["./docker/entrypoint.sh"]