from setuptools import setup, find_packages

setup(
    name="api_gateway",
    version="0.1.0",
    description="API Gateway for Python Microservice Demo",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "grpcio",
        "protobuf",
        "grpcio-tools",
    ],
    python_requires=">=3.8",
)
