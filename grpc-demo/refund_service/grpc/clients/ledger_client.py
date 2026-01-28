from generated_pb2 import ledger_pb2, ledger_pb2_grpc

class LedgerClient:
    def __init__(self, request, registry):
        self.request = request
        self.registry = registry

    async def record_refund(self):
        ledger = self.registry.get("ledger")

        return await ledger.RecordRefund(
            ledger_pb2.LedgerRequest(
                payment_id=self.request.order_id,
                amount=self.request.amount,
                method="CARD_PAYMENT_REFUND",
            ),
            timeout=2.0,
        )
