from fastapi import FastAPI
import threading
from .grpc_server import serve


app = FastAPI()


@app.on_event("startup")
def start_grpc():
    threading.Thread(target=serve, daemon=True).start()


@app.get("/health")
def health():
    return {"payment": "ok"}

