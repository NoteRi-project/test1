#!/usr/bin/env bash
set -euo pipefail

# Quick lint+build check for the frontend.
# Assumes dependencies are already installed (e.g. `npm install`).

cd "$(dirname "$0")/../frontend"

npm run lint
npm run build
