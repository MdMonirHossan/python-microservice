"""
Shared Authentication Utilities for All Services

This module provides:
- JWT token validation for gRPC requests
- Service authentication middleware
- Token scope verification
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any
from concurrent import futures
import grpc
from generated_pb2 import ledger_pb2, ledger_pb2_grpc, payment_pb2, payment_pb2_grpc, refund_pb2, refund_pb2_grpc


# Configuration
JWT_SECRET_KEY = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"


def create_service_token(service_id: str, scopes: list[str] = None) -> str:
    """
    Create a JWT token for service-to-service communication.
    
    Args:
        service_id: The ID of the service
        scopes: List of required scopes
    
    Returns:
        str: Encoded JWT token
    """
    now = datetime.utcnow()
    
    payload = {
        "sub": service_id,
        "scopes": scopes or ["service:read"],
        "iat": now,
        "exp": now + timedelta(minutes=30),
        "type": "service_token"
    }
    
    return create_access_token(payload)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    """Create a JWT token (helper function)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Dict[str, Any]:
    """
    Validate and decode a JWT token.
    
    Args:
        token: The JWT token to validate
    
    Returns:
        dict: The decoded token payload
    
    Raises:
        grpc.RpcError: If token is invalid or expired
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, "Token has expired")
    except jwt.InvalidTokenError:
        raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")


def check_scopes(payload: Dict[str, Any], required_scopes: list[str]) -> None:
    """
    Check if token has required scopes.
    
    Args:
        payload: The decoded token payload
        required_scopes: List of required scopes
    
    Raises:
        grpc.RpcError: If scopes are missing
    """
    token_scopes = payload.get("scopes", [])
    
    if not any(scope in token_scopes for scope in required_scopes):
        raise grpc.RpcError(
            grpc.StatusCode.PERMISSION_DENIED,
            f"Insufficient permissions. Required: {required_scopes}"
        )


class ServiceAuthInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    """
    gRPC Server Interceptor for JWT authentication.
    
    This interceptor validates JWT tokens on all incoming gRPC calls.
    """
    
    def __init__(self):
        # Define required scopes per service and RPC method
        self.scope_requirements = {
            "PaymentService": {
                "CreatePayment": ["payment:write"],
            },
            "LedgerService": {
                "RecordTransaction": ["ledger:write"],
                "RecordRefund": ["ledger:write"],
            },
            "RefundService": {
                "CreateRefund": ["refund:write"],
            }
        }
    
    async def intercept_unary_unary(self, continuation, call, request, context):
        """
        Intercept and validate incoming gRPC calls.
        
        Args:
            continuation: The next interceptor in the chain
            call: The RPC call
            request: The request message
            context: The RPC context
        
        Returns:
            The response from the service
        
        Raises:
            grpc.RpcError: If authentication fails
        """
        # Get authorization header
        auth_header = context.metadata.get('authorization', [''])[0]
        
        if not auth_header or not auth_header.startswith('Bearer '):
            raise grpc.RpcError(
                grpc.StatusCode.UNAUTHENTICATED,
                "Missing or invalid authorization header"
            )
        
        # Extract and validate token
        token = auth_header[len('Bearer '):]
        payload = verify_token(token)
        
        # Get service name from call description
        service_name = call.invocation_metadata[1][1] if len(call.invocation_metadata) > 1 else "UnknownService"
        method_name = call.invocation_metadata[2][1] if len(call.invocation_metadata) > 2 else "UnknownMethod"
        
        # Check scopes if requirements are defined
        if service_name in self.scope_requirements:
            if method_name in self.scope_requirements[service_name]:
                required_scopes = self.scope_requirements[service_name][method_name]
                check_scopes(payload, required_scopes)
        
        # Continue with the call
        return await continuation(request, context)


class ClientAuthInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    """
    gRPC Client Interceptor for adding authentication headers.
    
    This interceptor adds the service token to all outgoing gRPC calls.
    """
    
    def __init__(self, token: str):
        self.token = token
    
    async def intercept_unary_unary(self, continuation, call, request, context):
        """
        Add authentication header to outgoing calls.
        
        Args:
            continuation: The next interceptor in the chain
            call: The RPC call
            request: The request message
            context: The RPC context
        
        Returns:
            The response from the service
        """
        # Add authorization header
        context.with_compression(grpc.Compression.Gzip)
        
        return await continuation(request, context)
