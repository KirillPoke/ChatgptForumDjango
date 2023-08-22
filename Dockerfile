FROM python:3.11-slim-bullseye

WORKDIR /app
COPY . /app
COPY venv /app/venv

ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="/app/venv/bin:$PATH"

CMD ["pip", "freeze"]