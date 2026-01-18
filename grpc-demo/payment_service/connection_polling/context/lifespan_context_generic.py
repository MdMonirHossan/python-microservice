import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from generated_pb2 import payment_pb2_grpc
# from ...grpc_server import PaymentService
from ..grpc.server import PaymentService
from ..registry.grpc_registry import GrpcClientRegistry
from ..options.grpc_client_options import GRPC_OPTIONS
from ..registry.service_catalog import SERVICE_CATALOG

registry = GrpcClientRegistry(GRPC_OPTIONS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async lifespan context manager for FastAPI to initialize and close resources..

    - Startup: Connect to the grpc client
    - Yield: hands control to the app while it serves requests.
    - Shutdown: Close grpc client connection.
    Parameters:
    - app: FastAPI application instance.
    """
    print("🚀 Payment Service startup")

    # =============================================
    # Register ALL downstream services dynamically
    # =============================================
    for name, cfg in SERVICE_CATALOG.items():
        await registry.register(
            name=name,
            stub_cls=cfg["stub"],
            target=cfg["target"],
        )

    # =================================
    # Start Payment gRPC server
    # =================================
    grpc_server = grpc.aio.server()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(registry),
        grpc_server,
    )

    grpc_server.add_insecure_port("[::]:50051")
    await grpc_server.start()

    print("✅ Payment gRPC server STARTED on port 50051")

    app.state.grpc_server = grpc_server

    try:
        yield
    finally:
        # ============= Shutdown code ================
        print("🛑 Payment Service shutdown")

        # Stop accepting new gRPC requests
        await grpc_server.stop(grace=5)

        # Close all outbound gRPC channels
        await registry.close_all()