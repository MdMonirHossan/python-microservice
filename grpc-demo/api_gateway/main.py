from fastapi import FastAPI
import grpc
from generated_pb2 import payment_pb2, payment_pb2_grpc


app = FastAPI()


@app.post("/pay")
def create_payment(order_id: str, amount: float):
    channel = grpc.insecure_channel("localhost:50051")
    stub = payment_pb2_grpc.PaymentServiceStub(channel)

    response = stub.CreatePayment(
        payment_pb2.PaymentRequest(
            order_id=order_id,
            amount=amount
        )
    )

    print('Got response form payment', response)

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }

@app.post("/async-pay")
async def async_create_payment(order_id: str, amount: int):
    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:
        stub = payment_pb2_grpc.PaymentServiceStub(channel)

        response = await stub.CreatePayment(
            payment_pb2.PaymentRequest(
                order_id=order_id,
                amount=amount
            )
        )

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }