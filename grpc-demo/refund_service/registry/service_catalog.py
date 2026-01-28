from generated_pb2 import ledger_pb2_grpc

SERVICE_CATALOG = {
    "ledger": {
        "stub": ledger_pb2_grpc.LedgerServiceStub,
        # "target": "ledger:50052",
        "target": "localhost:50052",  
    },
}
