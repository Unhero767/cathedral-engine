#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Phase 1: Zero-Risk Quarantine Migration
# Non-destructively relocates stray, malformed, and duplicate copy files.
# ==============================================================================
set -euo pipefail

BASE_DIR="/users/kennethdallmier/cathedral_engine"
TARGET_DIR="${BASE_DIR}/quarantine_archive/phase_1_stray_and_duplicates"

echo "=== [CATHEDRAL ENGINE] Initializing Phase 1 Quarantine ==="
mkdir -p "${TARGET_DIR}"

safe_move() {
    local item="$1"
    if [ -e "${BASE_DIR}/${item}" ] || [ -L "${BASE_DIR}/${item}" ]; then
        echo "--> Quarantining: ${item}"
        mv "${BASE_DIR}/${item}" "${TARGET_DIR}/"
    else
        echo "    [Skip] Not found: ${item}"
    fi
}

# 1. Malformed and accidental shell escapes
safe_move "**DOMAIN**:"
safe_move "**PRIMARY"
safe_move "Cathedral"
safe_move "nul"
safe_move "1'"
safe_move "123"
safe_move "untitled folder"
safe_move "sercer.py"

# 2. Crash logs and backup dumps
safe_move "server.py.bak"
safe_move "server.py.err"

# 3. Redundant drafts and copy duplicates
safe_move "DESIGN copy.md"
safe_move "DESIGN 2.md"
safe_move "DESIGN 3.md"
safe_move "cathedral copy.py"
safe_move "cathedral_atlas_generator copy.py"
safe_move "DialogueTestHarness copy.gd"
safe_move "DialogueTestHarness copy.gd.uid"
safe_move "project copy.godot"

echo "=== [CATHEDRAL ENGINE] Phase 1 Quarantine Completed Successfully ==="
echo "Quarantined items safely stored in: ${TARGET_DIR}"
