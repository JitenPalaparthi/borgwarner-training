FROM python:3.11-slim

# Avoid buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional) - keep slim
RUN apt-get update && apt-get install -y --no-install-recommends         ca-certificates         && rm -rf /var/lib/apt/lists/*

# Copy project
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY proto ./proto
COPY server ./server

# Generate gRPC stubs into server package
RUN python -m grpc_tools.protoc -I proto         --python_out=server --grpc_python_out=server proto/customer.proto

EXPOSE 50051

# DATABASE_URL is set in docker-compose to point at the db service
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/app         PORT=50051

CMD ["python", "-m", "server.app"]
