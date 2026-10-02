#!/usr/bin/env bash
# ==============================================================================
# CATHEDRAL-ENGINE // GOOGLE DRIVE SYNCHRONIZATION PIPELINE
# Governed by Lex I (The Never-Overwrite Doctrine: dPhi/dt > 0)
# ==============================================================================
set -euo pipefail

REPO_ROOT="/users/kennethdallmier/cathedral_engine"
cd "$REPO_ROOT"

echo "=== [Cathedral Drive Sync] Initializing Synchronization Schema ==="

# 1. Create rclone filter rules file to ignore build caches and quarantine
FILTER_FILE="$REPO_ROOT/04_pipeline_tools/maintenance/rclone_sync_filter.txt"
cat << 'FEOF' > "$FILTER_FILE"
# Exclude build caches, version control, and temporary migration dumps
- .godot/**
- .git/**
- **/__pycache__/**
- **/node_modules/**
- **/.DS_Store
- 04_pipeline_tools/maintenance/quarantine/**
- *.tmp
- *.log

# Include canonical numbered strata and top-level descriptors
+ 01_Lore_and_Codices/**
+ 01_MLAOS_and_Codex_Docs/**
+ 02_Code_and_Installers/**
+ 02_engine_core/**
+ 03_godot_client/**
+ 04_pipeline_tools/**
+ 05_web_interface/**
+ 06_strata_data/**
+ 07_dist_releases/**
+ 08_docs_research/**
+ README.md
+ project.godot
+ .gitignore
+ braided_pipeline_harness.py
+ verify_dependencies.py

# Exclude any other loose untracked files
- *
FEOF

echo "✓ Created sync filter rules at $FILTER_FILE"

# 2. Check for native macOS Google Drive for Desktop mount
CLOUD_STORAGE_DIR="$HOME/Library/CloudStorage/GoogleDrive-kennydallmier@gmail.com/My Drive"
if [ ! -d "$CLOUD_STORAGE_DIR" ]; then
    CLOUD_STORAGE_DIR="/Volumes/GoogleDrive/My Drive"
fi

if [ -d "$CLOUD_STORAGE_DIR" ]; then
    echo "✓ Detected Google Drive for Desktop at: $CLOUD_STORAGE_DIR"
    TARGET_DRIVE_DIR="$CLOUD_STORAGE_DIR/MLAOS_Prime/cathedral_engine"
    mkdir -p "$TARGET_DRIVE_DIR"
    
    echo "Syncing via rsync (safe dry-run first)..."
    rsync -avPn --exclude-from="$FILTER_FILE" "$REPO_ROOT/" "$TARGET_DRIVE_DIR/"
    echo ""
    echo "To perform live local sync, run:"
    echo "rsync -avP --exclude-from=\"$FILTER_FILE\" \"$REPO_ROOT/\" \"$TARGET_DRIVE_DIR/\""
fi

# 3. Check for rclone CLI configuration
if command -v rclone &> /dev/null; then
    echo -e "\n=== rclone Configuration Detected ==="
    # Replace 'gdrive' with your configured remote name if different
    RCLONE_REMOTE="gdrive:MLAOS_Prime/cathedral_engine"
    echo "Dry-run command:"
    echo "rclone copy \"$REPO_ROOT\" \"$RCLONE_REMOTE\" --filter-from=\"$FILTER_FILE\" --drive-use-trash -P --dry-run"
    echo ""
    echo "Live sync command:"
    echo "rclone copy \"$REPO_ROOT\" \"$RCLONE_REMOTE\" --filter-from=\"$FILTER_FILE\" --drive-use-trash -P"
else
    echo -e "\nℹ️ rclone is not installed in current PATH."
    echo "You can use the native macOS Google Drive for Desktop rsync command above, or install rclone via: brew install rclone"
fi

echo "=== [Cathedral Drive Sync] Schema Generation Complete ==="
