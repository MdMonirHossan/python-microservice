from generated_pb2 import payment_pb2, payment_pb2_grpc
from generated_pb2 import ledger_pb2, ledger_pb2_grpc

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):
    """
    An asynchronous implementation of the PaymentService.

    This service coordinates payment processing by delegating transaction 
    recording to an external Ledger service. It utilizes dependency injection 
    for the Ledger client to facilitate better testing and resource management.

    Attributes:
        ledger_client: An initialized gRPC client wrapper used to communicate 
            with the Ledger service.
    """

    def __init__(self, ledger_stub):
        """
        Initializes the PaymentService with a ledger stub.

        Args:
            ledger_stub: An object containing a gRPC stub for Ledger operations.
        """
        self.ledger_stub = ledger_stub


    async def CreatePayment(self, request, context):
        """
        Processes a payment request asynchronously.

        This method orchestrates the following steps:
        1. Prepares a LedgerRequest based on the incoming payment data.
        2. Calls the LedgerService's RecordTransaction method with a 2-second timeout.
        3. Returns a confirmation of payment creation.

        Args:
            request: The payment details from the client (amount, etc.).
            context: The gRPC async context for the current call.

        Returns:
            payment_pb2.PaymentResponse: The status and ID of the created payment.

        Raises:
            grpc.RpcError: If the Ledger service call fails or times out.
        """
        payment_id = "pay_123"

        # Prepare the request for the downstream service
        request = ledger_pb2.LedgerRequest(
            payment_id=payment_id,
            amount=request.amount
        )

        # Execute the cross-service call with a deadline
        # The 'await' ensures this thread isn't blocked while waiting for the network
        await self.ledger_stub.RecordTransaction(
            request,
            timeout=2.0
        )

        return payment_pb2.PaymentResponse(
            payment_id=payment_id,
            status="CREATED"
        )
