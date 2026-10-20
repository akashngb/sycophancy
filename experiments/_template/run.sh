#!/usr/bin/env bash
# Run this experiment from anywhere.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../.."
uv run syco run --config "$HERE/config.yaml" "$@"
