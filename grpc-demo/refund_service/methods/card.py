from ..methods.base import RefundMethod
from generated_pb2 import refund_pb2
from ..grpc.clients.ledger_client import LedgerClient

class CardPaymentRefund(RefundMethod):
    async def process(self, request, registry):
        # Call Ledger service (Client)
        ledger = LedgerClient(request, registry)
        await ledger.record_refund()

        print(f"[REFUND] Payment ID: {request.payment_id}, Amount: {request.amount}")
        return refund_pb2.RefundResponse(
            refund_id=request.payment_id,
            success=True,
        )
