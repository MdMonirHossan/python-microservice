GRPC_OPTIONS = [
    # Send a keepalive ping every 30 seconds | Only if the connection is idle (no RPC traffic)
    # NATs, load balancers, firewalls silently drop idle TCP connections | This prevents “connection suddenly died” errors
    ("grpc.keepalive_time_ms", 30000),    # 30 Second

    # Wait 10 seconds for ping ACK | If not received → consider connection dead
    # Fast detection of dead peers | Avoid long hangs on broken connections
    ("grpc.keepalive_timeout_ms", 10000),   # 10 Second

    # Send keepalive pings even when no RPC is in progress
    # Prevent idle disconnects | Required for low-traffic services
    ("grpc.keepalive_permit_without_calls", 1), 
    
    # Forces periodic reconnection
    # Prevents stale / half-dead TCP connections
    # Important behind LBs & service meshes
    ("grpc.max_connection_idle_ms", 300000),      # 5 min
    ("grpc.max_connection_age_ms", 1800000),      # 30 min
    ("grpc.max_connection_age_grace_ms", 30000),  # 30 sec


    ("grpc.http2.max_pings_without_data", 0),
    ("grpc.http2.min_time_between_pings_ms", 10000),
    ("grpc.http2.min_ping_interval_without_data_ms", 10000),

    ("grpc.max_send_message_length", 10 * 1024 * 1024),
    ("grpc.max_receive_message_length", 10 * 1024 * 1024),
]
