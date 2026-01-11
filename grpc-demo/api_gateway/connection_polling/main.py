from fastapi import FastAPI
from .grpc_client import PaymentClient

app = FastAPI()

payment_client = PaymentClient("localhost:50051")

@app.on_event("startup")
async def startup():
    print('-------- on startupf ---- ', await payment_client.connect())
    await payment_client.connect()

@app.on_event("shutdown")
async def shutdown():
    await payment_client.close()

@app.post("/pay")
async def create_payment(order_id: str, amount: int):
    response = await payment_client.stub.CreatePayment(
        order_id=order_id,
        amount=amount,
        # timeout=2.0
    )

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }
