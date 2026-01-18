from generated_pb2 import payment_pb2, payment_pb2_grpc
from ..methods import METHOD_REGISTRY

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    def __init__(self, registry):
        self.registry = registry

    async def CreatePayment(self, request, context):
        handler = METHOD_REGISTRY[request.method]
        return await handler.process(request, self.registry)
