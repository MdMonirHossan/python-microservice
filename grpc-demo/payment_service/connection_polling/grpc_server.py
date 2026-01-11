from generated_pb2 import payment_pb2, payment_pb2_grpc

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):

    def __init__(self, ledger_client):
        self.ledger_client = ledger_client

    async def CreatePayment(self, request, context):
        payment_id = "pay_123"

        await self.ledger_client.stub.RecordTransaction(
            payment_id=payment_id,
            amount=request.amount
        )

        return payment_pb2.PaymentResponse(
            payment_id=payment_id,
            status="CREATED"
        )
