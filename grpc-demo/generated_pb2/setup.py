from setuptools import setup, find_packages

setup(
    name="generated_pb2",
    version="0.1.0",
    description="Generated Protobuf files for Python Microservice Demo",
    packages=find_packages(),
    install_requires=[
        "grpcio",
        "protobuf",
    ],
)
