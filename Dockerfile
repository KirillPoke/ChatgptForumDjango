FROM python:3.11-slim-bullseye as venv-installation-image
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY pyproject.toml poetry.lock poetry.toml ./

RUN pip install poetry && poetry install
FROM python:3.11-slim-bullseye
WORKDIR /app

COPY . /app
# Copy the settings here because the git context of buildx action ignores file modifications before the build
COPY infrastructure/cloud_local_settings.py /app/django_server/local_settings.py
COPY --from=venv-installation-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT ["bash", "entrypoint.sh"]


