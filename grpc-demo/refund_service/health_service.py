"""
gRPC Health Check Service Implementation

This service implements the gRPC health check protocol (grpc.health.v1.Health)
to allow other services to check if this service is healthy.
"""
from concurrent import futures
import grpc
from generated_pb2 import refund_pb2_grpc, refund_pb2


class HealthService(refund_pb2_grpc.HealthServicer):
    """
    Implements the gRPC health check protocol.
    
    This service allows other services to query the health status of this service.
    """
    
    def Check(self, request, context):
        """
        Check the health status of this service.
        
        Args:
            request: The HealthCheckRequest message
            context: The RPC context
            
        Returns:
            HealthCheckResponse: The health status
        """
        # In a real implementation, you would check the actual service health
        # For now, we always return SERVING
        return refund_pb2.HealthCheckResponse(status=refund_pb2.HealthCheckResponse.SERVING)
    
    def Watch(self, request, context):
        """
        Watch for health changes over time.
        
        Args:
            request: The HealthCheckRequest message
            context: The RPC context
            
        Returns:
            HealthCheckResponse stream: Health status changes
        """
        # For this implementation, we just return SERVING
        while True:
            yield refund_pb2.HealthCheckResponse(status=refund_pb2.HealthCheckResponse.SERVING)


def serve():
    """
    Start the health check server on port 50054.
    
    This server runs alongside the main service and exposes health checks.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    refund_pb2_grpc.add_HealthServicer_to_server(
        HealthService(), server
    )
    server.add_insecure_port("[::]:50054")
    server.start()
    print("gRPC Health Check Service running on port 50054")
    return server
