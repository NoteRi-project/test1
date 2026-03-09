#!/usr/bin/env bash
set -euo pipefail

# Quick syntax check for backend Python modules.
# On macOS, Python is typically available as `python3`.

cd "$(dirname "$0")/.."

python3 -m compileall backend
