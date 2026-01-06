from fastapi import FastAPI
import threading

from .lifespan_context import lifespan


app = FastAPI(title="Payment Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"payment": "ok"}

