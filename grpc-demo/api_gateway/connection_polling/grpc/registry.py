# shared gRPC registry
import grpc
from typing import Dict, Type

class GrpcClientRegistry:
    def __init__(self, options):
        self._options = options
        self._channels = {}
        self._stubs = {}

    async def register(self, name: str, stub_cls, target: str):
        if name in self._stubs:
            return self._stubs[name]

        channel = grpc.aio.insecure_channel(
            target,
            options=self._options,
        )

        stub = stub_cls(channel)

        self._channels[name] = channel
        self._stubs[name] = stub

        return stub

    def get(self, name: str):
        return self._stubs[name]

    async def close_all(self):
        for channel in self._channels.values():
            await channel.close()
