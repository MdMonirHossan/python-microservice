from fastapi import FastAPI, HTTPException
import grpc
from .common.grpc.single_grpc_client import PaymentClient
from generated_pb2 import payment_pb2, ledger_pb2
from .context.lifespan_context_single_client import payment_client, lifespan
from .context.lifespan_context_multi_client import lifespan as multi_client_lifespan
from .context.lifespan_context_generic import lifespan as lifespan_generic
from .grpc.catalog import SERVICE_CATALOG

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
        amount=amount
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
    cfg = SERVICE_CATALOG["create_payment"]

    stub = app.state.grpc_registry.get(cfg["service"])

    request = cfg["request_cls"](
        order_id=order_id,
        amount=amount,
    )
    print('------ cfg - ', cfg, '------- stub - ', stub, '------ request - ', request)
    try:
        rpc = getattr(stub, cfg["method"])
        print('--------------- rpc -- ', rpc)
        response = await rpc(request, timeout=2.0)
        print('---------------- resposne ---- ', response)

    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"{cfg['service']} service unavailable: {e.code().name}",
        )

    return {
        "payment_id": response.payment_id,
        "status": response.status,
    }
