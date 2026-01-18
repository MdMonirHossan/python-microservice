import grpc
from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..options.grpc_client_options import GRPC_OPTIONS
from ..common.registry.service_catalog import SERVICE_CATALOG
from ..common.grpc.client_registry_generic import GrpcClientRegistry

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

    try:
        yield
    finally:
        # ============= Shutdown code ================
        print("🛑 Payment Service shutdown")

        # Close all outbound gRPC channels
        await registry.close_all()