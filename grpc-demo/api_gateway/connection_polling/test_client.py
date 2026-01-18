import asyncio
import grpc
from ...generated_pb2 import payment_pb2, payment_pb2_grpc

async def test():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = payment_pb2_grpc.PaymentServiceStub(channel)
        res = await stub.CreatePayment(
            payment_pb2.PaymentRequest(order_id="1", amount=100, method="CARD"),
            timeout=2.0
        )
        print(res)

asyncio.run(test())
