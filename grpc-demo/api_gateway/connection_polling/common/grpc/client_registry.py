import grpc
from typing import Dict, Type

class GrpcClientRegistry:
    """
    A registry for managing the lifecycle of asynchronous gRPC channels and stubs.

    This class ensures that channels and stubs are reused based on their name, 
    preventing the overhead of creating multiple connections to the same target.
    """
    def __init__(self):
        """
        Initializes the registry with empty storage for channels and stubs.
        """
        self._channels: Dict[str, grpc.aio.Channel] = {}
        self._stubs = {}

    async def get_channel(self, name: str, target: str, options):
        if name not in self._channels:
            self._channels[name] = grpc.aio.insecure_channel(
                target, 
                options=options
            )
        return self._channels[name]

    async def get_stub(self, name: str, stub_cls, target, options):
        if name not in self._stubs:
            channel = await self.get_channel(name, target, options)
            self._stubs[name] = stub_cls(channel)
        return self._stubs[name]

    async def close_all(self):
        for channel in self._channels.values():
            await channel.close()
