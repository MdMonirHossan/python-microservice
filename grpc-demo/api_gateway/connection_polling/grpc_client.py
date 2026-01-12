import grpc
from generated_pb2 import payment_pb2_grpc

class PaymentClient:
    def __init__(self, target: str):
        self._target = target
        self._channel = None
        self._stub = None

    async def connect(self):
        if not self._channel:
            self._channel = grpc.aio.insecure_channel(
                self._target,
                # These control HTTP/2 keepalive pings between client ↔ server.
                options=[
                    # Send a keepalive ping every 30 seconds | Only if the connection is idle (no RPC traffic)
                    # NATs, load balancers, firewalls silently drop idle TCP connections | This prevents “connection suddenly died” errors
                    ("grpc.keepalive_time_ms", 30000),    # 30 Second

                    # Wait 10 seconds for ping ACK | If not received → consider connection dead
                    # Fast detection of dead peers | Avoid long hangs on broken connections
                    ("grpc.keepalive_timeout_ms", 10000),   # 10 Second

                    # Send keepalive pings even when no RPC is in progress
                    # Prevent idle disconnects | Required for low-traffic services
                    ("grpc.keepalive_permit_without_calls", 1), 
                    
                    # Forces periodic reconnection
                    # Prevents stale / half-dead TCP connections
                    # Important behind LBs & service meshes
                    ("grpc.max_connection_idle_ms", 300000),      # 5 min
                    ("grpc.max_connection_age_ms", 1800000),      # 30 min
                    ("grpc.max_connection_age_grace_ms", 30000),  # 30 sec
                ]
            )
            self._stub = payment_pb2_grpc.PaymentServiceStub(self._channel)

    async def close(self):
        if self._channel:
            await self._channel.close()

    @property
    def stub(self):
        if not self._stub:
            raise RuntimeError("PaymentClient not connected")
        return self._stub
    

# grpc.aio.insecure_channel(
#     target,
#     options=[
#         ("grpc.keepalive_time_ms", 30000),
#         ("grpc.keepalive_timeout_ms", 10000),
#         ("grpc.keepalive_permit_without_calls", 1),
#     ],
# )

