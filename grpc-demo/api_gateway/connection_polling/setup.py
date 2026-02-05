from setuptools import setup, find_packages

setup(
    name="api_gateway",
    version="0.1.0",
    description="API Gateway for Python Microservice Demo with JWT Authentication",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    package_dir={
        "api_gateway.connection_polling": "api_gateway/connection_polling",
        "generated_pb2": "../generated_pb2",
    },
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "grpcio",
        "protobuf",
        "pyjwt",
        "python-jose[cryptography]",
    ],
    python_requires=">=3.8",
)
