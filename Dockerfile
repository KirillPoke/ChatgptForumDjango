FROM python:3.11-slim-bullseye

WORKDIR /app
COPY . /app
ENV VIRTUAL_ENV=/app/venv
RUN ls /app/venv/bin
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["pip", "freeze"]