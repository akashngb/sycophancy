#!/usr/bin/env bash
# Starter flip-rate experiment. Run from the repo root.
set -euo pipefail
cd "$(dirname "$0")/../.."
uv run syco run --config configs/experiments/flip_rate_tiny.yaml "$@"
