#!/usr/bin/env bash
set -euo pipefail

# Fail if repo contains obvious private key headers.
# Exclude this script itself to avoid self-matching.

patterns=(
  'BEGIN OPENSSH PRIVATE KEY'
  'BEGIN RSA PRIVATE KEY'
  'BEGIN EC PRIVATE KEY'
  'BEGIN DSA PRIVATE KEY'
)

exclude_dirs=(.git frontend/node_modules backend/.venv .venv node_modules dist build)

exclude_args=()
for d in "${exclude_dirs[@]}"; do
  exclude_args+=("--exclude-dir=$d")
done
exclude_args+=("--exclude=$(basename "$0")")

for p in "${patterns[@]}"; do
  if grep -R -n --fixed-string "${exclude_args[@]}" "$p" . >/dev/null; then
    echo "ERROR: Detected private key material (pattern: $p)." >&2
    exit 1
  fi
done

echo "OK: no private key headers detected."
