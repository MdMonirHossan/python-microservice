import grpc
from concurrent import futures
from generated_pb2 import ledger_pb2, ledger_pb2_grpc


class LedgerService(ledger_pb2_grpc.LedgerServiceServicer):
    def RecordTransaction(self, request, context):
        print(f"[LEDGER] Payment {request.payment_id}, Amount {request.amount}")
        return ledger_pb2.LedgerResponse(success=True)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ledger_pb2_grpc.add_LedgerServiceServicer_to_server(
        LedgerService(), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()