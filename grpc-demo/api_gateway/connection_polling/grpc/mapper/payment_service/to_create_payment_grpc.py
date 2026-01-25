# HTTP → gRPC mapping
from generated_pb2 import payment_pb2

def to_create_payment_grpc(payload: dict) -> payment_pb2.PaymentRequest:
    return payment_pb2.PaymentRequest(
        order_id=payload["order_id"],
        amount=float(payload["amount"]),
        method=payload["method"],
    )