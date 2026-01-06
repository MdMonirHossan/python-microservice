import logging
import grpc
from concurrent import futures
from generated_pb2 import payment_pb2, payment_pb2_grpc
from generated_pb2 import ledger_pb2, ledger_pb2_grpc



class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    def CreatePayment(self, request, context):
        payment_id = "pay_123"

        channel = grpc.insecure_channel("localhost:50052")
        ledger_stub = ledger_pb2_grpc.LedgerServiceStub(channel)

        ledger_stub.RecordTransaction(
            ledger_pb2.LedgerRequest(
                payment_id=payment_id,
                amount=request.amount
            )
        )

        return payment_pb2.PaymentResponse(
            payment_id=payment_id,
            status="CREATED"
        )
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

