from fastapi import FastAPI
from .grpc_server import serve
from .context.lifespan_context_single_client import lifespan
from .context.lifespan_context_generic import lifespan as lifespan_generic

# For single client (Sync)
app = FastAPI(title="Ledger", lifespan=lifespan)

# For multi client (Async)
# app = FastAPI(title="Ledger", lifespan=lifespan_generic)

# For

@app.get("/health")
def health():
    return {"ledger": "ok"}