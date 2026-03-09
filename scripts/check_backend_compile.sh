#!/usr/bin/env bash
set -euo pipefail

# Quick syntax check for backend Python modules.
# On macOS, Python is typically available as `python3`.

cd "$(dirname "$0")/.."

if command -v python >/dev/null 2>&1; then
  python -m compileall backend
else
  python3 -m compileall backend
fi
