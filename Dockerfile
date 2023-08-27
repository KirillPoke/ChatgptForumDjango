FROM python:3.11-slim-bullseye

WORKDIR /app
COPY . .
COPY venv /app/venv

ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV

CMD ["pip", "freeze"]