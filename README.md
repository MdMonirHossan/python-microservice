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
