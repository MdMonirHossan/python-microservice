from generated_pb2 import payment_pb2, payment_pb2_grpc
from generated_pb2 import ledger_pb2, ledger_pb2_grpc

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):

    def __init__(self, ledger_client):
        self.ledger_client = ledger_client

    async def CreatePayment(self, request, context):
        payment_id = "pay_123"

        request = ledger_pb2.LedgerRequest(
            payment_id=payment_id,
            amount=request.amount
        )

        await self.ledger_client.stub.RecordTransaction(
            request,
            # timeout=2.0
        )

        return payment_pb2.PaymentResponse(
            payment_id=payment_id,
            status="CREATED"
        )
