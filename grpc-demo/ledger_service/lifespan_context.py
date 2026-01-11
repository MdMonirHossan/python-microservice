import threading
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

# from .grpc_server import serve
from .async_grpc_server import serve

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

    grpc_server = await serve()
    app.state.grpc_server = grpc_server

    try:
        yield       # Application handles requests during this phase
    finally:
        # ============= Shutdown code ================
        print("🛑 Application shutdown")
        await grpc_server.stop(grace=5)

