FROM python:3.11-slim-bullseye
EXPOSE 443
WORKDIR /app
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY pyproject.toml poetry.lock poetry.toml /app/
RUN pip install poetry && poetry install  --no-cache
COPY . /app
# Copy the settings here because the git context of buildx action ignores file modifications before the build
COPY infrastructure/cloud_local_settings.py /app/django_server/local_settings.py
RUN python manage.py diffsettings --all
RUN python manage.py collectstatic

ENTRYPOINT ["bash", "entrypoint.sh"]


