import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from generated_pb2 import payment_pb2_grpc

from ..common.grpc.single_grpc_client import LedgerClient
from ..grpc_server import PaymentService

ledger_client = LedgerClient("localhost:50052")

@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Async lifespan context manager for FastAPI to initialize and close resources..

    - Startup: start grpc server
    - Yield: hands control to the app while it serves requests.
    - Shutdown: logs application shutdown.
    Parameters:
    - app: FastAPI application instance.
    """
    # ============ Startup code ==============
    print("🚀 Application startup")
    
    # Start gRPC client (Ledger)
    await ledger_client.connect()

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
        print("🛑 Application shutdown")

        # Stop gRPC server first (stop accepting requests)
        await grpc_server.stop(grace=5)

        # Close gRPC client channels
        await ledger_client.close()

