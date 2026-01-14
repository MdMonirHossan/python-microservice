from fastapi import FastAPI
import asyncio
import grpc
from .grpc_server import PaymentService
from .common.grpc.single_grpc_client import LedgerClient
from generated_pb2 import payment_pb2_grpc

app = FastAPI()

ledger_client = LedgerClient("localhost:50052")

@app.on_event("startup")
async def startup():
    await ledger_client.connect()

    server = grpc.aio.server()
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(ledger_client), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()

    app.state.grpc_server = server

@app.on_event("shutdown")
async def shutdown():
    await ledger_client.close()
    await app.state.grpc_server.stop(5)

@app.get("/health")
async def health():
    return {"payment": "ok"}
