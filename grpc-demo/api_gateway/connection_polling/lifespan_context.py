import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .grpc_client import PaymentClient

payment_client = PaymentClient("localhost:50051")

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
    
    await payment_client.connect()

    try:
        yield       # Application handles requests during this phase
    finally:
        # ============= Shutdown code ================
        print("🛑 Application shutdown")
        await payment_client.close()

    