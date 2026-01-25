# Defines available gRPC services
"""
SERVICE_REGISTRY

Defines all downstream gRPC services known to the API Gateway.

This file answers the question:
👉 "How do I connect to a service?"

It does NOT:
- define which RPC to call
- define request/response mapping
"""
from generated_pb2 import payment_pb2_grpc

SERVICE_REGISTRY = {
    "payment": {
        "stub": payment_pb2_grpc.PaymentServiceStub,
        "target": "localhost:50051",
    },
    # "ledger": {
    #     "stub": ledger_pb2_grpc.LedgerServiceStub,
    #     "target": "localhost:50052",
    # },
}
