from fastapi import FastAPI
import asyncio
import grpc
from .context.lifespan import lifespan

# For One GRPC Client
# app = FastAPI(title="Payment Service", lifespan=lifespan)

# For Multi GRPC Client
# app = FastAPI(title="Payment Service", lifespan=multi_client_lifespan)

# For Multi GRPC Client Generics
app = FastAPI(title="Payment Service", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"payment": "ok"}
