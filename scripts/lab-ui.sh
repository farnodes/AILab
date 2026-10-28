#!/usr/bin/env bash
# AILab roadmap UI (curriculum + local progress)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/app/server.py"
