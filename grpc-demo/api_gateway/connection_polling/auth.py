"""
JWT Authentication Module for API Gateway

This module handles:
- JWT token generation for inter-service communication
- Token validation for incoming requests
- Token scope management
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from jose import JWTError, jwt
from starlette.requests import Request


# Configuration
JWT_SECRET_KEY = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_TOKEN_PREFIX = "Bearer"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for inter-service communication.
    
    Args:
        data: The data to encode in the token (e.g., service_id, scopes)
        expires_delta: Custom expiration time
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_bearer_token(request: Request) -> Optional[str]:
    """
    Extract and validate Bearer token from request headers.
    
    Args:
        request: FastAPI request object
    
    Returns:
        str: The extracted token, or None if not found/invalid
    
    Raises:
        HTTPException: If token is missing or invalid
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not auth_header.startswith(JWT_TOKEN_PREFIX + " "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication scheme. Use '{JWT_TOKEN_PREFIX} <token>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header[len(JWT_TOKEN_PREFIX + " "):]
    return token


async def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate and decode a JWT token.
    
    Args:
        token: The JWT token to validate
    
    Returns:
        dict: The decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token_scopes(payload: Dict[str, Any], required_scopes: list[str]) -> bool:
    """
    Verify that the token has the required scopes.
    
    Args:
        payload: The decoded token payload
        required_scopes: List of required scopes
    
    Returns:
        bool: True if all required scopes are present
    
    Raises:
        HTTPException: If scopes are missing
    """
    token_scopes = payload.get("scopes", [])
    
    # Check if user has any of the required scopes
    if not any(scope in token_scopes for scope in required_scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required scopes: {required_scopes}"
        )
    
    return True


async def generate_service_token(
    service_id: str,
    scopes: Optional[list[str]] = None,
    expires_in_minutes: int = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    """
    Generate a JWT token for service-to-service communication.
    
    Args:
        service_id: The ID of the service requesting the token
        scopes: List of scopes/permissions required
        expires_in_minutes: Token expiration time in minutes
    
    Returns:
        str: Generated JWT token
    """
    now = datetime.utcnow()
    
    payload = {
        "sub": service_id,
        "scopes": scopes or ["service:read"],
        "iat": now,
        "exp": now + timedelta(minutes=expires_in_minutes),
        "type": "service_token"
    }
    
    return create_access_token(payload, expires_delta=timedelta(minutes=expires_in_minutes))


async def verify_service_token(token: str) -> Dict[str, Any]:
    """
    Verify a service token and ensure it has the correct type.
    
    Args:
        token: The service token to verify
    
    Returns:
        dict: The decoded token payload
    
    Raises:
        HTTPException: If token is invalid or not a service token
    """
    payload = await validate_token(token)
    
    if payload.get("type") != "service_token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token type. Expected service token"
        )
    
    return payload
