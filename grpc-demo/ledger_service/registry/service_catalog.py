from generated_pb2 import payment_pb2_grpc

SERVICE_CATALOG = {
    "payment": {
        "stub": payment_pb2_grpc.PaymentServiceStub,
        # "target": "payment:50051",
        "target": "localhost:50051",
    },
}
