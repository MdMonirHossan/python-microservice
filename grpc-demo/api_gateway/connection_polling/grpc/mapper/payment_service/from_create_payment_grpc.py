# gRPC → HTTP mapping
"""
Payment mappers.

This file isolates protobuf usage from HTTP routes.
Routes NEVER import protobufs directly.
"""
from generated_pb2 import payment_pb2

def from_create_payment_grpc(response) -> dict:
    """
    Convert gRPC PaymentResponse to HTTP response dict.

    Args:
        response (PaymentResponse): Protobuf response

    Returns:
        dict: JSON-serializable HTTP response
    """
    return {
        "payment_id": response.payment_id,
        "status": response.status,
    }