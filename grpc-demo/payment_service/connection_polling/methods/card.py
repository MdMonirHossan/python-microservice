from ..methods.base import PaymentMethod
from generated_pb2 import ledger_pb2, payment_pb2
from ..grpc.clients.ledger_client import LedgerClient

class CardPayment(PaymentMethod):
    async def process(self, request, registry):
        # Call Ledger service (Client)
        ledger = LedgerClient(request, registry)
        led = await ledger.record_transaction()

        print(f"[PAYMENT] Payment {request.order_id}, Amount {request.amount}")
        return payment_pb2.PaymentResponse(
            payment_id=request.order_id,
            status="CREATED"
        )
