import grpc
from generated_pb2 import ledger_pb2, ledger_pb2_grpc

class LedgerClient:
    def __init__(self, target: str):
        self._target = target
        self._channel = None
        self._stub = None

    async def connect(self):
        if not self._channel:
            self._channel = grpc.aio.insecure_channel(self._target)
            self._stub = ledger_pb2_grpc.LedgerServiceStub(self._channel)

    async def close(self):
        if self._channel:
            await self._channel.close()

    @property
    def stub(self):
        if not self._stub:
            raise RuntimeError("LedgerClient not connected")
        return self._stub
