from ..methods.base import PaymentMethod
from generated_pb2 import ledger_pb2, payment_pb2

class CardPayment(PaymentMethod):
    async def process(self, request, registry):
        ledger = registry.get("ledger")

        await ledger.RecordTransaction(
            ledger_pb2.LedgerRequest(
                payment_id=request.order_id,
                amount=request.amount,
            ),
            timeout=2.0,
        )
        print(f"[PAYMENT] Payment {request.order_id}, Amount {request.amount}")
        return payment_pb2.PaymentResponse(
            payment_id=request.order_id,
            status="CREATED"
        )
