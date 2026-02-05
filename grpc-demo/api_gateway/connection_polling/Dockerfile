FROM python:3.11-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY api_gateway/connection_polling/setup.py .

# Install service dependencies
RUN pip install --no-cache-dir -e .

# Copy generated protobuf files
COPY generated_pb2/*.py ./generated_pb2/

# Copy application code
COPY api_gateway/connection_polling/*.py .
COPY api_gateway/connection_polling/common/*.py ./common/
COPY api_gateway/connection_polling/common/registry/*.py ./common/registry/
COPY api_gateway/connection_polling/common/grpc/*.py ./common/grpc/
COPY api_gateway/connection_polling/context/*.py ./context/
COPY api_gateway/connection_polling/context/lifespan_context*.py .
COPY api_gateway/connection_polling/grpc/*.py .
COPY api_gateway/connection_polling/grpc/mapper/*.py ./grpc/mapper/
COPY api_gateway/connection_polling/grpc/mapper/payment_service/*.py ./grpc/mapper/payment_service/
COPY api_gateway/connection_polling/grpc/mapper/refund_service/*.py ./grpc/mapper/refund_service/
COPY api_gateway/connection_polling/grpc/registry.py .
COPY api_gateway/connection_polling/grpc/action_catalog.py .
COPY api_gateway/connection_polling/options/setup.py ./options/
COPY api_gateway/connection_polling/options/grpc_client_options.py .

# Expose HTTP port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
