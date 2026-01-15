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

    # Create Ledger gRPC client (channel + stub)
    ledger_stub = await registry.get_stub(
        name="ledger",
        stub_cls=ledger_pb2_grpc.LedgerServiceStub,
        target="localhost:50052",
        options=GRPC_OPTIONS,
    )

    app.state.ledger_stub = ledger_stub

    # Start Payment gRPC server
    grpc_server = grpc.aio.server()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(ledger_stub),
        grpc_server,
    )

    grpc_server.add_insecure_port("[::]:50051")
    await grpc_server.start()

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


    