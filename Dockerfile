FROM python:3.11-slim-bullseye

WORKDIR /app
COPY . /app
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

CMD ["pip", "freeze"]