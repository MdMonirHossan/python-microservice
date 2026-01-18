from ..methods.base import PaymentMethod
from generated_pb2 import ledger_pb2

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

        return {"status": "CARD_SUCCESS"}
