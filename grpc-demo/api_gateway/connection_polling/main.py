from fastapi import FastAPI, HTTPException
import grpc
from .grpc_client import PaymentClient
from generated_pb2 import payment_pb2, ledger_pb2
from .lifespan_context import payment_client, lifespan
from .lifespan_context_multi_client import lifespan as multi_client_lifespan

# Connect with single grpc client
# app = FastAPI(title="API Gateway", lifespan=lifespan)

# Connect with multi grpc client
app = FastAPI(title="API Gateway", lifespan=multi_client_lifespan)

@app.post("/pay")
async def create_payment(order_id: str, amount: int):
    
    request = payment_pb2.PaymentRequest(
        order_id=order_id,
        amount=amount
    )
    try:
        # =================== single client ================
        # response = await payment_client.stub.CreatePayment(
        #     request,
        #     timeout=2.0
        # )


        # ============== Multi Client (Payment Service) ==========
        response = await app.state.payment_stub.CreatePayment(
            request,
            timeout=2.0
        )
        print('------------------ got resposne --- ', response)

        # Ledger Service
        payment_id = "pay_123"

        led_request = ledger_pb2.LedgerRequest(
            payment_id=payment_id,
            amount=amount
        )

        led_response = await app.state.ledger_stub.RecordTransaction(
            led_request,
            timeout=2.0
        )
        print('------------------ got resposne for ledger_response --- ', led_response)
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Payment service unavailable: {e.code().name}"
        )

    return {
        "payment_id": response.payment_id,
        "status": response.status
    }
