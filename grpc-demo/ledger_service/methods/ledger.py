from ..methods.base import LedgerMethod
from generated_pb2 import ledger_pb2, payment_pb2

class LedgerEntry(LedgerMethod):
    async def process(self, request, registry):
        print(f"[LEDGER] Payment {request.payment_id}, Amount {request.amount}")
        return ledger_pb2.LedgerResponse(success=True)
