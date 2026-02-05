FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY ledger_service/setup.py .
COPY ledger_service/methods/setup.py ./methods/

# Install service dependencies
RUN pip install --no-cache-dir -e .

# Copy generated protobuf files
COPY generated_pb2/*.py ./generated_pb2/

# Copy application code
COPY ledger_service/*.py .
COPY ledger_service/methods/*.py ./methods/
COPY ledger_service/health_service.py .
COPY ledger_service/context/*.py ./context/
COPY ledger_service/registry/*.py ./registry/

# Expose gRPC port
EXPOSE 50052

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import grpc; grpc.insecure_channel('localhost:50052')" || exit 1

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "50052"]
