# gRPC → HTTP mapping
from generated_pb2 import payment_pb2

def from_create_payment_grpc(response) -> dict:
    return {
        "payment_id": response.payment_id,
        "status": response.status,
    }