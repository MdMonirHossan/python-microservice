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
        """
        Retrieves an existing gRPC channel or creates a new one if it doesn't exist.

        Args:
            name: A unique identifier for the channel.
            target: The server address (e.g., 'localhost:50051').
            options: A list of key-value pairs to configure the channel.

        Returns:
            grpc.aio.Channel: The asynchronous gRPC channel associated with the name.
        """
        if name not in self._channels:
            self._channels[name] = grpc.aio.insecure_channel(
                target, 
                options=options
            )
        return self._channels[name]

    async def get_stub(self, name: str, stub_cls, target, options):
        """
        Retrieves an existing gRPC stub or creates a new one.

        This method automatically ensures the underlying channel is created first.

        Args:
            name: A unique identifier for the stub.
            stub_cls: The gRPC Stub class (e.g., MyServiceStub).
            target: The server address if the channel needs to be created.
            options: Configuration options for the channel creation.

        Returns:
            Any: An instance of the provided stub_cls.
        """
        if name not in self._stubs:
            channel = await self.get_channel(name, target, options)
            self._stubs[name] = stub_cls(channel)
        return self._stubs[name]

    async def close_all(self):
        """
        Closes all registered gRPC channels gracefully.

        Should be called during application shutdown to ensure all network
        resources are released.
        """
        for channel in self._channels.values():
            await channel.close()
