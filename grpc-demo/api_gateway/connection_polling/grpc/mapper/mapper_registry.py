"""
MAPPER_REGISTRY

Maps action names to their request/response mapper functions.
"""
from .payment_service import (
    to_create_payment_grpc,
    from_create_payment_grpc,
)

from .refund_service import (
    to_create_refund_grpc,
    from_create_refund_grpc,
)

MAPPER_REGISTRY = {
    "create_payment": {
        "to_grpc": to_create_payment_grpc.to_create_payment_grpc,
        "from_grpc": from_create_payment_grpc.from_create_payment_grpc,
    },
    "create_refund": {
        "to_grpc": to_create_refund_grpc.to_create_refund_grpc,
        "from_grpc": from_create_refund_grpc.from_create_refund_grpc,
    },
    # "refund_payment": {
    #     "to_grpc": to_refund_payment_grpc,
    #     "from_grpc": from_refund_payment_grpc,
    # },
}