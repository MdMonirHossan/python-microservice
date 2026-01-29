# HTTP → gRPC mapping
"""
Refund mappers.

This file isolates protobuf usage from HTTP routes.
Routes NEVER import protobufs directly.
"""
from generated_pb2 import refund_pb2

def to_create_refund_grpc(payload: dict) -> refund_pb2.RefundRequest:
    """
    Convert HTTP request payload to gRPC RefundRequest.

    Args:
        payload (dict): HTTP request body or query params

    Returns:
        RefundRequest: Protobuf request object
    """
    return refund_pb2.RefundRequest(
        payment_id=payload["payment_id"],
        amount=float(payload["amount"]),
        method=payload["method"],
    )