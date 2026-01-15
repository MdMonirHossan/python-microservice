import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from generated_pb2 import payment_pb2_grpc
from ...grpc_server import PaymentService
from ..registry.grpc_registry import GrpcClientRegistry
from ..options.grpc_client_options import GRPC_OPTIONS
from ..registry.service_catalog import SERVICE_CATALOG

registry = GrpcClientRegistry(GRPC_OPTIONS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Payment Service startup")

    # 1️⃣ Register ALL downstream services dynamically
    for name, cfg in SERVICE_CATALOG.items():
        await registry.register(
            name=name,
            stub_cls=cfg["stub"],
            target=cfg["target"],
        )

    # 2️⃣ Start Payment gRPC server
    grpc_server = grpc.aio.server()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(registry),
        grpc_server,
    )

    grpc_server.add_insecure_port("[::]:50051")
    await grpc_server.start()

    app.state.grpc_server = grpc_server

    try:
        yield
    finally:
        print("🛑 Payment Service shutdown")
        await grpc_server.stop(grace=5)
        await registry.close_all()