# Infrastructure & DevOps Improvements

This document describes the infrastructure improvements implemented to enhance service communication in the gRPC demo project.

## 🚀 Phase 1: Infrastructure & DevOps

### 1. Containerization with Docker

All services have been containerized with optimized Dockerfiles:

#### Services
- **payment_service**: Container running on port 50051
- **ledger_service**: Container running on port 50052
- **refund_service**: Container running on port 50053
- **api_gateway**: Container running on port 8000

#### Docker Features
- Multi-stage builds for optimized images
- Health checks configured in Dockerfiles
- Non-root user for security
- Minimal base image (python:3.11-slim)

### 2. Service Orchestration with Docker Compose

A comprehensive `docker-compose.yml` file orchestrates all services:

```bash
docker-compose up -d
```

#### Features
- Automatic service startup and dependency management
- Health checks for service readiness
- Network isolation with a dedicated bridge network
- Automatic restart policies
- Environment variable configuration

#### Network Configuration
- Services communicate over a private bridge network (`grpc_network`)
- Service discovery via Docker's internal DNS
- No hardcoded IPs - services use service names as hostnames

### 3. gRPC Health Checks

All services now implement the gRPC health check protocol (`grpc.health.v1.Health`):

#### Endpoints
- HTTP: `/health` on each service
- gRPC: Health check service on ports 50051-50053

#### Usage
```bash
# Check all services
curl http://localhost:8000/health

# gRPC health check
grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check
```

### 4. JWT Authentication

#### API Gateway
- Extracts and validates JWT tokens from incoming requests
- Generates service tokens for downstream services
- Enforces per-route scope requirements
- Secure token handling with environment variables

#### Service Authentication
- Server-side interceptors validate tokens on all gRPC calls
- Scope-based authorization
- Token expiration and validation
- Per-service and per-method scope requirements

#### Token Generation
```python
from common.auth_client import ServiceTokenProvider

token_provider = ServiceTokenProvider("service_name")
token = token_provider.get_token_for_service("target_service")
```

### 5. DNS-Based Service Discovery

#### Configuration
- Services use Docker service names as hostnames
- Automatic resolution via Docker's internal DNS
- Environment variable configuration for flexibility

#### Service URLs
- `payment_service` → `payment:50051`
- `ledger_service` → `ledger:50052`
- `refund_service` → `refund:50053`
- `api_gateway` → `gateway:8000`

#### Benefits
- No hardcoded service IPs
- Easy multi-instance scaling
- Better service isolation
- Native Docker integration

### 6. Common Infrastructure Modules

#### `common/auth_utils.py`
- Shared authentication utilities
- Token validation and creation
- Scope verification
- Server and client interceptors

#### `common/auth_client.py`
- Service token generation
- Client interceptors with authentication
- Token provider pattern

#### `common/config.py`
- Centralized service configuration
- Environment variable management
- Service URL generation
- Local and Docker configurations

## 📋 Usage Guide

### Prerequisites
- Docker and Docker Compose installed
- gRPC tools (grpcurl for testing)

### Setup

1. **Build and start all services:**
```bash
docker-compose build
docker-compose up -d
```

2. **Wait for services to be healthy:**
```bash
docker-compose ps
```

3. **Test the API Gateway:**
```bash
# Health check
curl http://localhost:8000/health

# Create a payment (requires JWT token)
curl -X POST http://localhost:8000/pay \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "order_id=123&amount=100"

# Create a refund
curl -X POST http://localhost:8000/refund \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "payment_id=pay_123&amount=100"
```

### Service Discovery Testing

```bash
# Test payment service from another service
grpcurl -plaintext payment:50051 payment.PaymentService/CreatePayment -d '{"order_id":"test","amount":100}'

# Test ledger service
grpcurl -plaintext ledger:50052 ledger.LedgerService/RecordTransaction -d '{"payment_id":"test","amount":100}'
```

## 🔧 Configuration

### Environment Variables

Configure services via environment variables:

```yaml
# In docker-compose.yml
services:
  payment_service:
    environment:
      - LEDGER_SERVICE_HOST=ledger
      - LEDGER_SERVICE_PORT=50052
```

### JWT Configuration

Update the secret key in a secure environment:

```yaml
api_gateway:
  environment:
    - JWT_SECRET_KEY=your-secure-secret-key-here
    - JWT_ALGORITHM=HS256
```

## 🛡️ Security Features

### Authentication Flow
1. Client sends request with Bearer token to API Gateway
2. Gateway validates token and checks scopes
3. Gateway generates service token for downstream service
4. Service token is included in gRPC metadata
5. Downstream service validates token via interceptor
6. Request proceeds if authorized

### Token Scope Requirements
- `/pay`: Requires `payment:write` scope
- `/pay-dynamic`: Requires `payment:write` scope
- `/refund`: Requires `refund:write` scope

## 📊 Monitoring & Health

### Service Health Checks

```bash
# Check all services
docker-compose ps

# Check specific service logs
docker-compose logs -f payment_service
docker-compose logs -f ledger_service
docker-compose logs -f refund_service
docker-compose logs -f api_gateway
```

### gRPC Health Check Protocol

```bash
# Check payment service
grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check

# Check ledger service
grpcurl -plaintext localhost:50052 grpc.health.v1.Health/Check

# Check refund service
grpcurl -plaintext localhost:50053 grpc.health.v1.Health/Check
```

## 🚀 Scaling

### Multi-Instance Scaling

```bash
# Run multiple instances of payment service
docker-compose up -d --scale payment_service=3
```

Services automatically discover each other via Docker DNS.

### Load Balancing

Docker Compose handles service discovery automatically. Use a reverse proxy like Nginx for HTTP load balancing.

## 🐛 Troubleshooting

### Service Not Starting

```bash
# Check service logs
docker-compose logs payment_service

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Connection Issues

```bash
# Verify network connectivity
docker-compose exec payment_service ping ledger

# Test DNS resolution
docker-compose exec payment_service getent hosts ledger
```

### Authentication Issues

1. Ensure JWT_SECRET_KEY is set correctly
2. Check token expiration times
3. Verify token scopes match required permissions

## 📝 Next Steps (Phase 2)

1. **Load Balancing**: Implement client-side load balancing with multiple service instances
2. **Observability**: Add Prometheus metrics and structured logging with correlation IDs
3. **Per-Method Timeouts**: Configure individual timeout values for different RPC methods
4. **Circuit Breakers**: Implement resilience patterns for failed services
5. **Request Compression**: Enable gRPC compression for message optimization

## 📚 References

- [Docker Documentation](https://docs.docker.com/)
- [gRPC Health Checks](https://github.com/grpc/grpc-go/blob/master/health/grpc_health_v1/health.proto)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Service Discovery Patterns](https://microservices.io/patterns/service-discovery.html)
