FROM python:3.11-slim-bullseye AS venv-image
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY poetry.toml poetry.lock pyproject.toml entrypoint.sh ./
ENV VIRTUAL_ENV=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV
RUN pip install poetry && poetry install
ENTRYPOINT ["bash", "entrypoint.sh"]

FROM python:3.11-slim-bullseye as app-image
EXPOSE 80
WORKDIR /app
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV
COPY --from=venv-image /.venv $VIRTUAL_ENV
COPY . /app


# Copy the settings here because the git context of buildx action ignores file modifications before the build
#COPY infrastructure/cloud_local_settings.py /app/django_server/local_settings.py

ENTRYPOINT ["bash", "entrypoint.sh"]


