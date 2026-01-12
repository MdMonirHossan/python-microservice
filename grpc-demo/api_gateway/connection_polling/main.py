from fastapi import FastAPI, HTTPException
import grpc
from .grpc_client import PaymentClient
from generated_pb2 import payment_pb2
from .lifespan_context import payment_client, lifespan

app = FastAPI(title="API Gateway", lifespan=lifespan)

@app.post("/pay")
async def create_payment(order_id: str, amount: int):
    
    request = payment_pb2.PaymentRequest(
        order_id=order_id,
        amount=amount
    )
    try:
        response = await payment_client.stub.CreatePayment(
            request,
            timeout=2.0
        )
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Payment service unavailable: {e.code().name}"
        )

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }
