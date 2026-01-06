import threading
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .grpc_server import serve

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
    print('------ Application Startup...')
    # threading.Thread(target=serve, daemon=True).start()

    asyncio.create_task(serve())
    
    yield       # Application handles requests during this phase

    # ============= Shutdown code ================