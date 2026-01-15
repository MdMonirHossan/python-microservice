from generated_pb2 import ledger_pb2_grpc

SERVICE_CATALOG = {
    "ledger": {
        "stub": ledger_pb2_grpc.LedgerServiceStub,
        "target": "ledger:50052",
    },
    # "fraud": {
    #     "stub": fraud_pb2_grpc.FraudServiceStub,
    #     "target": "fraud:50053",
    # },
    # "bank": {
    #     "stub": bank_pb2_grpc.BankServiceStub,
    #     "target": "bank:50054",
    # },
}
