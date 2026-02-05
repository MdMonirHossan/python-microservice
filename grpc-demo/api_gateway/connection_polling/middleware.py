"""
Authentication Middleware for API Gateway

This middleware:
- Extracts and validates JWT tokens from incoming requests
- Passes service tokens to downstream services
- Enforces authentication requirements
"""
from fastapi import Request, Response, status, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from typing import Callable
from .auth import (
    get_bearer_token,
    validate_token,
    verify_token_scopes,
    verify_service_token,
    JWT_TOKEN_PREFIX
)
from jose import JWTError


# CORS middleware configuration
CORS_CONFIG = {
    "allow_origins": ["*"],  # Configure properly in production
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


class JWTAuthMiddleware:
    """
    Middleware for JWT authentication.
    
    This middleware validates JWT tokens on all protected routes.
    """
    
    def __init__(self, app: Callable):
        self.app = app
        self.required_scopes = {
            "/pay": ["payment:write"],
            "/pay-dynamic": ["payment:write"],
            "/refund": ["refund:write"],
        }
    
    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        if scope["type"] == "http":
            request = Request(scope, receive)
            path = request.url.path
            
            # Check if route requires authentication
            if path in self.required_scopes:
                try:
                    # Get and validate token
                    token = await get_bearer_token(request)
                    payload = await validate_token(token)
                    
                    # Verify scopes
                    required_scopes = self.required_scopes[path]
                    verify_token_scopes(payload, required_scopes)
                    
                    # Add token to request state for downstream services
                    request.state.service_token = token
                    request.state.user = payload
                    
                except HTTPException:
                    # Re-raise HTTP exceptions
                    pass
                except JWTError:
                    # Return 401 for invalid tokens
                    from starlette.responses import JSONResponse
                    response = JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid or expired token"}
                    )
                    await response(scope, receive, send)
                    return
            
            # Add CORS headers
            response = await self.app(scope, receive, send)
            if hasattr(response, "headers"):
                response.headers["Access-Control-Allow-Origin"] = CORS_CONFIG["allow_origins"]
                response.headers["Access-Control-Allow-Credentials"] = str(
                    CORS_CONFIG["allow_credentials"]
                ).lower()
                response.headers["Access-Control-Allow-Methods"] = ",".join(
                    CORS_CONFIG["allow_methods"]
                )
                response.headers["Access-Control-Allow-Headers"] = ",".join(
                    CORS_CONFIG["allow_headers"]
                )
            
            return response
        
        # For non-HTTP requests, just pass through
        await self.app(scope, receive, send)


def add_cors_middleware(app: Callable) -> Callable:
    """
    Add CORS middleware to the FastAPI application.
    
    Args:
        app: The FastAPI application
    
    Returns:
        Callable: The middleware-protected application
    """
    return CORSMiddleware(
        app=app,
        allow_origins=CORS_CONFIG["allow_origins"],
        allow_credentials=CORS_CONFIG["allow_credentials"],
        allow_methods=CORS_CONFIG["allow_methods"],
        allow_headers=CORS_CONFIG["allow_headers"],
    )


def get_service_token(request: Request) -> str:
    """
    Get the service token from the request state.
    
    Args:
        request: The FastAPI request object
    
    Returns:
        str: The service token
    
    Raises:
        HTTPException: If no service token is found
    """
    if not hasattr(request.state, "service_token"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No service token provided"
        )
    
    return request.state.service_token
