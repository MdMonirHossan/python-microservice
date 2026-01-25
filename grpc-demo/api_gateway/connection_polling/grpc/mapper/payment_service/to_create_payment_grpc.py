# HTTP → gRPC mapping
"""
Payment mappers.

This file isolates protobuf usage from HTTP routes.
Routes NEVER import protobufs directly.
"""
from generated_pb2 import payment_pb2

def to_create_payment_grpc(payload: dict) -> payment_pb2.PaymentRequest:
    """
    Convert HTTP request payload to gRPC PaymentRequest.

    Args:
        payload (dict): HTTP request body or query params

    Returns:
        PaymentRequest: Protobuf request object
    """
    return payment_pb2.PaymentRequest(
        order_id=payload["order_id"],
        amount=float(payload["amount"]),
        method=payload["method"],
    )