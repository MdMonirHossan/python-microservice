from setuptools import setup, find_packages

setup(
    name="ledger_service",
    version="0.1.0",
    description="Ledger Service for Python Microservice Demo",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "grpcio",
        "protobuf",
    ],
    python_requires=">=3.8",
)
