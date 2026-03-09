#!/usr/bin/env bash
set -euo pipefail

# Build backend Docker image locally (no container run).
# Usage: ./scripts/docker_build.sh [tag]

cd "$(dirname "$0")/.."
TAG=${1:-test1-backend:local}

docker build -t "$TAG" .
