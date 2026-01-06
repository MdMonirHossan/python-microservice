from fastapi import FastAPI
import threading
from .grpc_server import serve
from .lifespan_context import lifespan


app = FastAPI(title="Ledger", lifespan=lifespan)


@app.get("/health")
def health():
    return {"ledger": "ok"}