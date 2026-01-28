from ..methods.base import RefundMethod
from generated_pb2 import ledger_pb2, payment_pb2
from ..grpc.clients.ledger_client import LedgerClient

class CardPaymentRefund(RefundMethod):
    async def process(self, request, registry):
        # Call Ledger service (Client)
        ledger = LedgerClient(request, registry)

        print(f"[REFUND] Order ID: {request.order_id}, Amount: {request.amount}")
        return payment_pb2.PaymentResponse(
            payment_id=request.order_id,
            status="REFUNDED"
        )
