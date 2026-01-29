#### Generate gRPC Code

Run from project root

```bash
  python -m grpc_tools.protoc \
  -I protos \
  --python_out=. \
  --grpc_python_out=. \
  protos/payment.proto protos/ledger.proto
```


### What Happens When You Add New Things?
**✅ Add a new gRPC service**

1. Add proto + stub
2. Add ONE entry in SERVICE_CATALOG
Done.

**✅ Add a new payment method**

1. Create new class in methods/
2. Register in METHOD_REGISTRY
Done.

#### ❌ No changes to:

- Lifespan
- PaymentService
- gRPC server
- Registry


API Gateway = Translator + Guard
Payment Service = Orchestrator
Ledger Service = Source of Truth

Server = inbound APIs
Client = outbound calls
Mapper = protocol translator
Registry = connection owner


### CURL Request
```bash
  curl -X POST "http://localhost:8000/pay-dynamic?order_id=ORD1&amount=525"

  curl -X POST "http://localhost:8000/refund?payment_id=pay_123&amount=100"

  curl -X POST "http://localhost:8000/pay-dynamic?order_id=order_123&amount=100"
```


### Make Python able to see generated_pb2/
Export PYTHONPATH (Local Dev)

#### From project root:
```bash
export PYTHONPATH=$(pwd)/generated_pb2:$(pwd)
```