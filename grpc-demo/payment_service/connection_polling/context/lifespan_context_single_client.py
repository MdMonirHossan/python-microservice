import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager

from ..common.grpc.single_grpc_client import LedgerClient

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

    # start GRPC server without async
    # threading.Thread(target=serve, daemon=True).start()
    # asyncio.create_task(serve())
    
    await ledger_client.connect()

    try:
        yield       # Application handles requests during this phase
    finally:
        # ============= Shutdown code ================
        print("🛑 Application shutdown")
        await ledger_client.close()