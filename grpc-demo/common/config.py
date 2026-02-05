"""
Service Discovery Configuration Module

This module provides:
- DNS-based service discovery configuration
- Environment variable management
- Service URL generation
"""
import os
from typing import Optional
from functools import lru_cache


class ServiceConfig:
    """Configuration for a specific service."""
    
    def __init__(self, service_name: str, default_port: int):
        self.service_name = service_name
        self.default_port = default_port
        self.hostname = os.getenv(f"{service_name.upper()}_HOST", service_name)
        self.port = int(os.getenv(f"{service_name.upper()}_PORT", default_port))
    
    @property
    def url(self) -> str:
        """Get the full service URL."""
        return f"{self.hostname}:{self.port}"
    
    @property
    def channel_target(self) -> str:
        """Get the gRPC channel target."""
        return self.url


class Config:
    """Central configuration for all services."""
    
    # Payment Service Configuration
    payment = ServiceConfig("payment", 50051)
    
    # Ledger Service Configuration
    ledger = ServiceConfig("ledger", 50052)
    
    # Refund Service Configuration
    refund = ServiceConfig("refund", 50053)
    
    # API Gateway Configuration
    gateway = ServiceConfig("gateway", 8000)
    
    @classmethod
    @lru_cache()
    def get_service_url(cls, service_name: str) -> str:
        """
        Get the URL for a specific service by name.
        
        Args:
            service_name: The name of the service
        
        Returns:
            str: The service URL
        
        Raises:
            ValueError: If service name is unknown
        """
        services = {
            "payment": cls.payment.url,
            "ledger": cls.ledger.url,
            "refund": cls.refund.url,
            "gateway": cls.gateway.url,
        }
        
        if service_name.lower() not in services:
            raise ValueError(f"Unknown service: {service_name}")
        
        return services[service_name.lower()]
    
    @classmethod
    def get_all_urls(cls) -> dict[str, str]:
        """
        Get URLs for all services.
        
        Returns:
            dict: Mapping of service names to URLs
        """
        return {
            "payment": cls.payment.url,
            "ledger": cls.ledger.url,
            "refund": cls.refund.url,
        }


# Default configuration for services running in Docker
DockerConfig = Config

# Configuration for local development
LocalConfig = Config
LocalConfig.payment.hostname = "localhost"
LocalConfig.ledger.hostname = "localhost"
LocalConfig.refund.hostname = "localhost"


def get_service_target(service_name: str) -> str:
    """
    Get the gRPC target for a service.
    
    This uses the service name as the hostname (DNS-based discovery).
    
    Args:
        service_name: The name of the service
    
    Returns:
        str: The gRPC target (service name)
    """
    # For Docker, use the service name as hostname
    # Docker automatically resolves service names to service IP
    return service_name
