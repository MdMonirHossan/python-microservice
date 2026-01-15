import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..options.grpc_client_options import GRPC_OPTIONS
from generated_pb2 import payment_pb2_grpc, ledger_pb2_grpc

from ..common.grpc.client_registry import GrpcClientRegistry
from ..grpc_server import PaymentService

# GRPC client Registry Instance
registry = GrpcClientRegistry()


@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Async lifespan context manager for FastAPI to initialize and close resources..

    - Startup: Connect to the grpc client
    - Yield: hands control to the app while it serves requests.
    - Shutdown: Close grpc client connection.
    Parameters:
    - app: FastAPI application instance.
    """
    # ============ Startup code ==============
    print("🚀 Application startup")

    # Connect GRPC Clients
    app.state.ledger_stub = await registry.get_stub(
        name="ledger",
        stub_cls=ledger_pb2_grpc.LedgerServiceStub,
        target="localhost:50052",
        options=GRPC_OPTIONS,
    )

    # Payment service config
    # Start gRPC server (Payment)
    grpc_server = grpc.aio.server()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(ledger_client),
        grpc_server
    )

    grpc_server.add_insecure_port("[::]:50051")
    await grpc_server.start()

    app.state.grpc_server = grpc_server

    try:
        yield       # Application handles requests during this phase
    finally:
        # ============= Shutdown code ================
        await registry.close_all()

    