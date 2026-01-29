# service + method mapping
from generated_pb2 import payment_pb2, payment_pb2_grpc
from generated_pb2 import refund_pb2, refund_pb2_grpc

SERVICE_CATALOG = {
    "payment_service": {
        "service": "payment",
        "stub": payment_pb2_grpc.PaymentServiceStub,
        # "target": "payment:50051",
        "target": "localhost:50051",
        "method": "CreatePayment",
        # "request_cls": payment_pb2.PaymentRequest,
    },
    "refund_service": {
        "service": "refund",
        "stub": refund_pb2_grpc.RefundServiceStub,
        # "target": "refund:50052",
        "target": "localhost:50053",
        "method": "CreateRefund",
    },
    # "refund_payment": {
    #     "service": "payment",
    #     "stub": payment_pb2_grpc.PaymentServiceStub,
    #     "target": "localhost:50051",
    #     "method": "RefundPayment",
    #     "request_cls": payment_pb2.RefundRequest,
    # }

}
