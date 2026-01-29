from generated_pb2 import ledger_pb2, ledger_pb2_grpc

class LedgerClient:
    """
    Ledger client for refund service
    """
    def __init__(self, request, registry):
        self.request = request
        self.registry = registry

    async def record_refund(self):
        """
        Record a refund in the ledger
        """
        ledger = self.registry.get("ledger")

        return await ledger.RecordRefund(
            ledger_pb2.LedgerRequest(
                payment_id=self.request.payment_id,
                amount=self.request.amount,
                method="LEDGER",
            ),
            timeout=2.0,
        )
