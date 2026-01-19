# HTTP → gRPC mapping
from generated_pb2 import payment_pb2

def http_to_payment_request(payload: dict) -> payment_pb2.PaymentRequest:
    return payment_pb2.PaymentRequest(
        order_id=payload["orderId"],
        amount=float(payload["amount"]),
        method=payload["paymentMethod"],
    )


def payment_response_to_http(response) -> dict:
    return {
        "payment_id": response.payment_id,
        "status": response.status,
    }
