import logging
import grpc
from concurrent import futures
from generated_pb2 import payment_pb2, payment_pb2_grpc, ledger_pb2_grpc, ledger_pb2


class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    
    async def CreatePayment(self, request, context):
        payment_id = "pay_123"

        async with grpc.aio.insecure_channel(
            "localhost:50052"
        ) as channel:
            ledger_stub = ledger_pb2_grpc.LedgerServiceStub(channel)

            await ledger_stub.RecordTransaction(
                ledger_pb2.LedgerRequest(
                    payment_id=payment_id,
                    amount=request.amount
                )
            )
        print(f"[PAYMENT] Payment {payment_id}, Amount {request.amount}")
        return payment_pb2.PaymentResponse(
            payment_id=payment_id,
            status="CREATED"
        )
    

async def serve() -> grpc.aio.Server:
    server = grpc.aio.server()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(), server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()

    logging.info("✅ gRPC server started on :50051")
    return server