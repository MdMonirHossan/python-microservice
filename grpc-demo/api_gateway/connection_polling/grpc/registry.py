# shared gRPC registry
# Manages gRPC channels & stubs
"""
GrpcClientRegistry

Responsible for:
- creating gRPC channels
- reusing them (connection pooling)
- closing them on shutdown
"""
import grpc
from typing import Dict, Type

class GrpcClientRegistry:
    def __init__(self, options):
        self._options = options
        self._channels = {}
        self._stubs = {}

    async def register(self, name: str, stub_cls, target: str):
        """
            Register a gRPC client if not already registered.
        """
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
        """
        Get an already-registered gRPC stub.
        """
        return self._stubs[name]

    async def close_all(self):
        """
        Close all gRPC channels gracefully.
        """
        for channel in self._channels.values():
            await channel.close()
