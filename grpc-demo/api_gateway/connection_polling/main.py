from fastapi import FastAPI
from .grpc_client import PaymentClient
from generated_pb2 import payment_pb2

app = FastAPI()

payment_client = PaymentClient("localhost:50051")

@app.on_event("startup")
async def startup():
    await payment_client.connect()

@app.on_event("shutdown")
async def shutdown():
    await payment_client.close()

@app.post("/pay")
async def create_payment(order_id: str, amount: int):
    
    request = payment_pb2.PaymentRequest(
        order_id=order_id,
        amount=amount
    )
    print('----------- request for payment ---- ', request)
    response = await payment_client.stub.CreatePayment(
        request,
        # timeout=2.0
    )

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }
