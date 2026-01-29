"""
Payment-related HTTP endpoints.

Routes do:
- choose action
- call mapper
- invoke gRPC
- return HTTP response

Routes do NOT:
- know protobuf fields
- contain business logic
"""
from fastapi import FastAPI, HTTPException
import grpc
from .common.grpc.single_grpc_client import PaymentClient
from generated_pb2 import payment_pb2, ledger_pb2
from .context.lifespan_context_single_client import payment_client, lifespan
from .context.lifespan_context_multi_client import lifespan as multi_client_lifespan
from .context.lifespan_context_generic import lifespan as lifespan_generic
from .grpc.service_catalog import SERVICE_CATALOG
from .grpc.action_catalog import ACTION_CATALOG
from .grpc.mapper.mapper_registry import MAPPER_REGISTRY
# from .grpc.mapper import http_to_payment_request, payment_response_to_http

# Connect with single grpc client
# app = FastAPI(title="API Gateway", lifespan=lifespan)

# Connect with multi grpc client
# app = FastAPI(title="API Gateway", lifespan=multi_client_lifespan)

# Connect with multi grpc client
app = FastAPI(title="API Gateway", lifespan=lifespan_generic)

@app.post("/pay")
async def create_payment(order_id: str, amount: int):
    
    # ===================== Payment Service (Service 01) ==================
    request = payment_pb2.PaymentRequest(
        order_id=order_id,
        amount=amount,
        method="CARD",
    )

    # ==================== Ledger Service (Service 02) ======================
    # payment_id = "pay_123"
    # led_request = ledger_pb2.LedgerRequest(
    #     payment_id=payment_id,
    #     amount=amount
    # )
    try:
        # =================== single client ================
        # response = await payment_client.stub.CreatePayment(
        #     request,
        #     timeout=2.0
        # )


        # ============== Multi Client (Payment Service 01) ==========
        response = await app.state.payment_stub.CreatePayment(
            request,
            timeout=2.0
        )
        print('------------------ got resposne --- ', response)

        # ======================== Ledger Service (02) =================

        # led_response = await app.state.ledger_stub.RecordTransaction(
        #     led_request,
        #     timeout=2.0
        # )
        # print('------------------ got resposne for ledger_response --- ', led_response)
        # ==================================== xxxx =============================
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Payment service unavailable: {e.code().name}"
        )

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }

@app.post("/pay-dynamic")
async def create_payment(order_id: str, amount: int):
    """
    This is a dynamic payment creation endpoint.
    It uses the action catalog to find the appropriate action and mapper.
    """
    action = "create_payment"

    action_cfg = ACTION_CATALOG[action]
    mapper = MAPPER_REGISTRY[action]
    
    stub = app.state.grpc_registry.get(
        action_cfg["service"]
    )

    grpc_request = mapper["to_grpc"]({
        "order_id": order_id,
        "amount": amount,
        "method": "CARD",
    })

    try:
        rpc = getattr(stub, action_cfg["rpc"])
        grpc_response = await rpc(
            grpc_request,
            timeout=action_cfg["timeout"],
        )
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"{action_cfg['service']} unavailable",
        )

    return mapper["from_grpc"](grpc_response)


@app.post("/refund")
async def create_refund(payment_id: str, amount: int):
    """
    This is a dynamic refund creation endpoint.
    It uses the action catalog to find the appropriate action and mapper.

    """
    action = "create_refund"

    action_cfg = ACTION_CATALOG[action]
    mapper = MAPPER_REGISTRY[action]
    
    stub = app.state.grpc_registry.get(
        action_cfg["service"]
    )

    grpc_request = mapper["to_grpc"]({
        "payment_id": payment_id,
        "amount": amount,
        "method": "CARD",
    })

    try:
        rpc = getattr(stub, action_cfg["rpc"])
        grpc_response = await rpc(
            grpc_request,
            timeout=action_cfg["timeout"],
        )
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"{action_cfg['service']} unavailable",
        )

    return mapper["from_grpc"](grpc_response)
