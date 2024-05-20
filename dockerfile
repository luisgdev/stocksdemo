FROM python:3.11-alpine3.19

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install poetry
RUN apk add make

ENV VIRTUAL_ENV "/opt/venv"

ENV PATH "$VIRTUAL_ENV/bin:$PATH"

COPY app/poetry.lock app/pyproject.toml /app/

RUN python -m venv $VIRTUAL_ENV \
  && poetry install --with=dev

COPY app /app
