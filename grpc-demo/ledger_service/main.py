from fastapi import FastAPI
from .grpc_server import serve
from .context.lifespan_context_single_client import lifespan

# For single client (Sync)
app = FastAPI(title="Ledger", lifespan=lifespan)

# For


@app.get("/health")
def health():
    return {"ledger": "ok"}