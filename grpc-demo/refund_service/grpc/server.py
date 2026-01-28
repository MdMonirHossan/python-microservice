import grpc
from generated_pb2 import refund_pb2, refund_pb2_grpc
from ..methods import METHOD_REGISTRY

class RefundService(refund_pb2_grpc.RefundServiceServicer):
    def __init__(self, registry):
        self.registry = registry
    
    async def CreateRefund(self, request, context):
        """
        Docstring for CreateRefund

        :param self: Description
        :param request: Description
        :param context: Description
        """
        try:
            handler = METHOD_REGISTRY[request.method]
            return await handler.process(request, self.registry)
        except KeyError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"Unknown payment method: {request.method}"
            )
        except Exception as e:
            await context.abort(
                grpc.StatusCode.INTERNAL,
                f"Internal error: {str(e)}"
            )
