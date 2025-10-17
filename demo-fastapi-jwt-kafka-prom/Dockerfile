FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential curl tini ca-certificates git     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY .env ./.env

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["/entrypoint.sh"]
