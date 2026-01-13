import json

"""
GRPC_OPTIONS: A list of configurations for the gRPC channel lifecycle.

Key Categories:
1. Keepalives: Prevents silent connection drops by firewalls/NATs.
2. Connection Aging: Forces rotation to ensure even load balancing across pods.
3. Message Size: Increases default 4MB limit to 10MB for heavy data transfers.
4. Client-Side Retries: Built-in resilience for transient network errors.
"""
GRPC_OPTIONS = [
    # ===== Keepalive Settings ======
    # Send a keepalive ping every 30 seconds | Only if the connection is idle (no RPC traffic)
    # NATs, load balancers, firewalls silently drop idle TCP connections | This prevents “connection suddenly died” errors
    ("grpc.keepalive_time_ms", 30000),    # 30 sec

    # Wait 10 seconds for ping ACK | If not received → consider connection dead
    # Fast detection of dead peers | Avoid long hangs on broken connections
    ("grpc.keepalive_timeout_ms", 10000),   # 10 sec

    # Send keepalive pings even when no RPC is in progress
    # Prevent idle disconnects | Required for low-traffic services
    ("grpc.keepalive_permit_without_calls", 1), 

    # ===== Connection Rotation (Critical for L4 Load Balancers) =====
    # If a connection is idle for 5 mins, close it.
    ("grpc.max_connection_idle_ms", 300000),      
    # Hard limit: Force a reconnect every 30 mins to re-balance traffic.
    ("grpc.max_connection_age_ms", 1800000),      
    # Allow 30s for active calls to finish before hard-closing after 'age' limit.
    ("grpc.max_connection_age_grace_ms", 30000), 

    # ===== HTTP/2 Protocol Protections ====
    # Prevent server from rejecting pings
    # Avoid HTTP/2 GOAWAY errors
    ("grpc.http2.max_pings_without_data", 0),
    ("grpc.http2.min_time_between_pings_ms", 10000),         # 10 sec
    ("grpc.http2.min_ping_interval_without_data_ms", 10000), # 10 sec

    # ==== Payload Constraints =====
    # Large payloads (statements, reconciliation)
    # Prevent unexpected failures
    ("grpc.max_send_message_length", 10 * 1024 * 1024),    # 10 MB
    ("grpc.max_receive_message_length", 10 * 1024 * 1024),

    # ===== Service Config & Retries =====
    ("grpc.enable_retries", 1),
    ("grpc.service_config", json.dumps({
        "methodConfig": [{
            "name": [{"service": "payment.PaymentService"}],
            "retryPolicy": {
                "maxAttempts": 4,
                "initialBackoff": "0.2s",
                "maxBackoff": "2s",
                "backoffMultiplier": 2,
                "retryableStatusCodes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"]
            }
        }]
    }))
]


READ_ONLY_RETRY_CONFIG = {
    "methodConfig": [{
        "name": [{"service": "ledger.LedgerService"}],
        "retryPolicy": {
            "maxAttempts": 3,
            "initialBackoff": "0.1s",
            "maxBackoff": "1s",
            "backoffMultiplier": 2,
            "retryableStatusCodes": ["UNAVAILABLE"]
        }
    }]
}
