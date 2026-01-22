import grpc
from generated_pb2 import ledger_pb2, ledger_pb2_grpc
from ..methods import METHOD_REGISTRY

class LedgerService(ledger_pb2_grpc.LedgerServiceServicer):
    def __init__(self, registry):
        self.registry = registry


    async def RecordTransaction(self, request, context):
        """
        Docstring for CreatePayment
        
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
            context.abort(
                grpc.StatusCode.INTERNAL,
                f"Internal error: {str(e)}"
            )
    
