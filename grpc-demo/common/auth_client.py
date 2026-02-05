"""
Client-side Authentication Utilities for Service-to-Service Calls

This module provides:
- Token generation for outgoing gRPC calls
- Client interceptors for adding authentication headers
"""
import grpc
from .auth_utils import create_service_token, ClientAuthInterceptor


class ServiceTokenProvider:
    """
    Provider for service tokens used in inter-service communication.
    
    Each service should have a token provider that can generate tokens
    for other services.
    """
    
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    def get_token_for_service(self, target_service: str, scopes: list[str] = None) -> str:
        """
        Get a token for a specific service.
        
        Args:
            target_service: The name of the service requesting the token
            scopes: Required scopes for the token
        
        Returns:
            str: Service token
        """
        return create_service_token(target_service, scopes)
    
    def get_client_interceptor(self, target_service: str, scopes: list[str] = None) -> ClientAuthInterceptor:
        """
        Get a client interceptor with authentication for a specific service.
        
        Args:
            target_service: The name of the service to authenticate with
            scopes: Required scopes for the token
        
        Returns:
            ClientAuthInterceptor: The interceptor with the token
        """
        token = self.get_token_for_service(target_service, scopes)
        return ClientAuthInterceptor(token)
