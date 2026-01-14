from fastapi import FastAPI
import asyncio
import grpc
from .grpc_server import PaymentService
from .common.grpc.single_grpc_client import LedgerClient
from generated_pb2 import payment_pb2_grpc
from .context.lifespan_context_single_client import lifespan 

app = FastAPI(title="Payment Service", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"payment": "ok"}
