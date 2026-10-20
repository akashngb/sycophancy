#!/usr/bin/env bash
# Quick end-to-end smoke test against the fake backend. No downloads.
set -euo pipefail
cd "$(dirname "$0")/.."
uv run syco run --config configs/experiments/flip_rate_fake.yaml
