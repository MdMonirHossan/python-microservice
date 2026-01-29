"""
Refund mappers.

This file isolates protobuf usage from HTTP routes.
Routes NEVER import protobufs directly.
"""
from generated_pb2 import refund_pb2

def from_create_refund_grpc(response: refund_pb2.RefundResponse) -> dict:
    """
    Convert gRPC RefundResponse to HTTP response dict.

    Args:
        response (RefundResponse): Protobuf response

    Returns:
        dict: JSON-serializable HTTP response
    """
    return {
        "refund_id": response.refund_id,
        "success": response.success,
    }