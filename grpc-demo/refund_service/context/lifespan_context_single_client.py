import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from generated_pb2 import refund_pb2_grpc
from ..grpc_server import RefundService
from ..common.auth_utils import ServiceAuthInterceptor

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
    
    # Start gRPC server (Refund)
    grpc_server = grpc.aio.server()

    # Add authentication interceptor
    grpc_server.add_interceptor(ServiceAuthInterceptor())

    refund_pb2_grpc.add_RefundServiceServicer_to_server(
        RefundService(), grpc_server
    )

    grpc_server.add_insecure_port("[::]:50053")
    await grpc_server.start()

    app.state.grpc_server = grpc_server

    try:
        yield       # Application handles requests during this phase
    finally:
        # ============= Shutdown code ================
        print("🛑 Application shutdown")

        # Stop gRPC server first (stop accepting requests)
        await grpc_server.stop(grace=5)
