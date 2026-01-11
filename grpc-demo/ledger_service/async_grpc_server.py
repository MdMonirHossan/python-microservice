import logging
import grpc
from concurrent import futures
from generated_pb2 import ledger_pb2, ledger_pb2_grpc


class LedgerService(ledger_pb2_grpc.LedgerServiceServicer):
    async def RecordTransaction(self, request, context):
        print(f"[LEDGER] Payment {request.payment_id}, Amount {request.amount}")
        return ledger_pb2.LedgerResponse(success=True)
    

async def serve() -> grpc.aio.Server:
    server = grpc.aio.server()

    ledger_pb2_grpc.add_LedgerServiceServicer_to_server(
        LedgerService(), server
    )

    server.add_insecure_port("[::]:50052")
    await server.start()

    logging.info("✅ gRPC server started on :50052")
    return server