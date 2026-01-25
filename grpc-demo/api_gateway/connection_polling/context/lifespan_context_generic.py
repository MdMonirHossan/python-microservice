import logging
import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..options.grpc_client_options import GRPC_OPTIONS
from ..grpc.service_catalog import SERVICE_CATALOG
from ..common.grpc.client_registry_generic import GrpcClientRegistry

logger = logging.getLogger(__name__)

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
    for cfg in SERVICE_CATALOG.values():
        await registry.register(
            name=cfg["service"],
            stub_cls=cfg["stub"],
            target=cfg["target"],
        )
        print(f""" => Registered Clients: 🚀{str(cfg["service"]).capitalize()} Service""")
    
    app.state.grpc_registry = registry

    try:
        yield
    finally:
        # ============= Shutdown code ================
        print("🛑 Payment Service shutdown")

        # Close all outbound gRPC channels
        await registry.close_all()

