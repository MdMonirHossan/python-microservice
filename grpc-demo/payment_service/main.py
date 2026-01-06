from fastapi import FastAPI

from .lifespan_context import lifespan


app = FastAPI(title="Payment Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"payment": "ok"}

