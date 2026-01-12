import grpc
from generated_pb2 import payment_pb2_grpc

class PaymentClient:
    def __init__(self, target: str):
        self._target = target
        self._channel = None
        self._stub = None

    async def connect(self):
        if not self._channel:
            self._channel = grpc.aio.insecure_channel(self._target)
            self._stub = payment_pb2_grpc.PaymentServiceStub(self._channel)

    async def close(self):
        if self._channel:
            await self._channel.close()

    @property
    def stub(self):
        if not self._stub:
            raise RuntimeError("PaymentClient not connected")
        return self._stub
    

# grpc.aio.insecure_channel(
#     target,
#     options=[
#         ("grpc.keepalive_time_ms", 30000),
#         ("grpc.keepalive_timeout_ms", 10000),
#         ("grpc.keepalive_permit_without_calls", 1),
#     ],
# )

