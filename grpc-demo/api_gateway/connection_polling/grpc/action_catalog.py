# Maps API actions → service + RPC
"""
ACTION_CATALOG

Maps a business action to:
- which service to call
- which gRPC RPC method to invoke
- which mapper to use
- timeout configuration

This file answers:
👉 "What should happen for this API action?"
"""
ACTION_CATALOG = {
    "create_payment": {
        "service": "payment",
        "rpc": "CreatePayment",
        "mapper": "create_payment",
        "timeout": 2.0,
    },
    "create_refund": {
        "service": "refund",
        "rpc": "CreateRefund",
        "mapper": "create_refund",
        "timeout": 2.0,
    },
    "get_payment_status": {
        "service": "payment",
        "rpc": "GetPaymentStatus",
        "mapper": "get_payment_status",
        "timeout": 1.0,
    },
}