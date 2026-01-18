from fastapi import FastAPI
import asyncio
import grpc
from .grpc_server import PaymentService
from .common.grpc.single_grpc_client import LedgerClient
from generated_pb2 import payment_pb2_grpc
from .context.lifespan_context_single_client import lifespan 
from .context.lifespan_context_multi_client import lifespan as multi_client_lifespan
from .context.lifespan_context_generic import lifespan as lifespan_generic

# For One GRPC Client
# app = FastAPI(title="Payment Service", lifespan=lifespan)

# For Multi GRPC Client
# app = FastAPI(title="Payment Service", lifespan=multi_client_lifespan)

# For Multi GRPC Client Generics
app = FastAPI(title="Payment Service", lifespan=lifespan_generic)

@app.get("/health")
async def health():
    return {"payment": "ok"}
