FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY payment_service/setup.py .
COPY payment_service/connection_polling/setup.py ./connection_polling
COPY payment_service/connection_polling/options/setup.py ./connection_polling/options

# Install service dependencies
RUN pip install --no-cache-dir -e .

# Copy generated protobuf files
COPY generated_pb2/*.py ./generated_pb2/

# Copy application code
COPY payment_service/connection_polling/*.py .
COPY payment_service/connection_polling/main.py .
COPY payment_service/connection_polling/grpc_server.py .
COPY payment_service/connection_polling/methods/*.py ./methods/
COPY payment_service/connection_polling/health_service.py .

# Expose gRPC port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import grpc; grpc.insecure_channel('localhost:50051')" || exit 1

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "50051"]
