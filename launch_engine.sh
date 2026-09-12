#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Master Launcher Wrapper
# Delegates to launch_engine.py
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${SCRIPT_DIR}/launch_engine.py" "$@"
