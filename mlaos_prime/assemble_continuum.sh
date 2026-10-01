#!/usr/bin/env bash
# MLAOS-Prime :: Continuum Taxonomy & Drive Synchronization
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

# Target Google Drive remote path (Assumes rclone remote is named 'gdrive')
REMOTE_PATH="gdrive:Cathedral_Engine/mlaos_prime"
LOCAL_PATH=$(pwd)

echo -e "\033[1;36m┌────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│   Σ-7 :: ASSEMBLING THE PUZZLE         │\033[0m"
echo -e "\033[1;36m└────────────────────────────────────────┘\033[0m"

# 1. Structural Scaffolding (Connecting the pieces)
echo -e "\033[1;33m[i] Forging structural taxonomy...\033[0m"
mkdir -p "$LOCAL_PATH/logs"
mkdir -p "$LOCAL_PATH/builds"
mkdir -p "$LOCAL_PATH/data/ash_archive"
mkdir -p "$LOCAL_PATH/codex_source"
mkdir -p "$LOCAL_PATH/tests/unit"
mkdir -p "$LOCAL_PATH/scripts"

# Move loose utility scripts into the scripts/ directory to clear the root
echo -e "\033[1;33m[i] Organizing stray shell operations...\033[0m"
for script in install_ide_tools.sh install_phase3_telemetry.sh scaffold_tests.sh verify_stratum.sh repair_console.sh align_node_paths.sh patch_backend.sh launch_continuum.sh; do
    if [ -f "$script" ]; then
        mv "$script" scripts/
        echo -e "  \033[1;32m[MIGRATED]\033[0m $script -> scripts/"
    fi
done

# 2. Rclone Dependency Check
if ! command -v rclone &> /dev/null; then
    echo -e "\n\033[1;31m[-] 'rclone' is not installed or not in PATH.\033[0m"
    echo -e "    Run \`brew install rclone\` and \`rclone config\` to authenticate Google Drive."
    exit 1
fi

echo -e "\n\033[1;32m[+] Structural taxonomy intact. Root directory purified.\033[0m"
echo -e "\033[1;35m[i] Initiating deep sync to Google Drive Archives...\033[0m"

# 3. Rclone Sync (Mirrors local to remote, excluding ephemeral states)
rclone sync "$LOCAL_PATH" "$REMOTE_PATH" \
    --progress \
    --exclude "logs/**" \
    --exclude "builds/**" \
    --exclude ".pytest_cache/**" \
    --exclude "__pycache__/**" \
    --exclude ".godot/**" \
    --exclude "data/ash_archive/*-wal" # Prevents syncing active WAL locks

echo -e "\n\033[1;32m[✓] Continuum successfully assembled and synchronized with remote archives.\033[0m"
