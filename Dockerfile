FROM python:3.11-slim-bullseye

WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install
COPY . /app



