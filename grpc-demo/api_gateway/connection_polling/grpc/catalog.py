# service + method mapping
from generated_pb2 import payment_pb2, payment_pb2_grpc
from ..options.grpc_client_options import GRPC_OPTIONS

SERVICE_CATALOG = {
    "create_payment": {
        "service": "payment",
        "stub": payment_pb2_grpc.PaymentServiceStub,
        # "target": "payment:50051",
        "target": "localhost:50051",
        "method": "CreatePayment",
        "request_cls": payment_pb2.PaymentRequest,
    },
    # "refund_payment": {
    #     "service": "payment",
    #     "stub": payment_pb2_grpc.PaymentServiceStub,
    #     "target": "localhost:50051",
    #     "method": "RefundPayment",
    #     "request_cls": payment_pb2.RefundRequest,
    # }

}
