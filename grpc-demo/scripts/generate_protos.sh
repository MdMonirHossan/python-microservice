#!/usr/bin/env bash
#
# Universal proto generation script (Python gRPC)
#
# Works with:
# - old grpcio-tools
# - new grpcio-tools
# - CI
# - Docker
#
# NO python_package
# NO python_opt
# NO sys.path hacks
#

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PROTO_DIR="$PROJECT_ROOT/protos"
OUT_DIR="$PROJECT_ROOT/generated_pb2"

echo "🚀 Generating Python gRPC code"
echo "📂 Protos:  $PROTO_DIR"
echo "📦 Output:  $OUT_DIR"

mkdir -p "$OUT_DIR"
touch "$OUT_DIR/__init__.py"

python -m grpc_tools.protoc \
  -I "$PROTO_DIR" \
  --python_out="$OUT_DIR" \
  --grpc_python_out="$OUT_DIR" \
  $(find "$PROTO_DIR" -name "*.proto")

echo "✅ Proto generation completed"
