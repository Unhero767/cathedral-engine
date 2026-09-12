#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Dynamic Master Consolidation Script (Track 2)
# Target: /Users/kennethdallmier/cathedral-engine/cathedral_engine_full_project
# ==============================================================================
set -euo pipefail

BASE_DIR="/Users/kennethdallmier/cathedral-engine"
TARGET_DIR="${BASE_DIR}/cathedral_engine_full_project"

echo "=== [CATHEDRAL ENGINE CONSOLIDATION] Initializing Dynamic Migration ==="

# 1. Directory Tree Scaffolding
mkdir -p "${TARGET_DIR}/autoload"
mkdir -p "${TARGET_DIR}/core/sync"
mkdir -p "${TARGET_DIR}/data/character_recipes"
mkdir -p "${TARGET_DIR}/scenes/chambers"
mkdir -p "${TARGET_DIR}/scenes/terminal"
mkdir -p "${TARGET_DIR}/scenes/world"
mkdir -p "${TARGET_DIR}/scripts/chambers"
mkdir -p "${TARGET_DIR}/scripts/terminal"
mkdir -p "${TARGET_DIR}/shaders"
mkdir -p "${TARGET_DIR}/strata"
mkdir -p "${TARGET_DIR}/systems/avatar"
mkdir -p "${TARGET_DIR}/systems/soulframe"

# Helper function to find and copy files recursively if exact folder names vary
find_and_copy() {
    local target_name="$1"
    local dest_path="$2"
    local found_path=""
    
    found_path=$(find "${BASE_DIR}" -name "${target_name}" -not -path "*/cathedral_engine_full_project/*" -print -quit 2>/dev/null || true)
    
    if [ -n "${found_path}" ]; then
        cp -v "${found_path}" "${dest_path}"
    else
        echo "[WARNING] Target file/directory not found across workspace: ${target_name}"
    fi
}

echo "--> [1/5] Locating and Migrating Global Signal Bus..."
find_and_copy "event_bus.gd" "${TARGET_DIR}/autoload/event_bus.gd"

echo "--> [2/5] Locating and Migrating Bio-Semantic Physics & Soulframe..."
find_and_copy "spectral_constants.gd" "${TARGET_DIR}/core/spectral_constants.gd"
find_and_copy "a_field_manager.gd" "${TARGET_DIR}/core/a_field_manager.gd"
find_and_copy "dialetheic_buffer.gd" "${TARGET_DIR}/core/dialetheic_buffer.gd"
find_and_copy "metamorphic_squeeze.gd" "${TARGET_DIR}/systems/metamorphic_squeeze.gd"
find_and_copy "harmonic_scar.gdshader" "${TARGET_DIR}/shaders/harmonic_scar.gdshader"

echo "--> [3/5] Locating and Migrating Gothic Terminal & VFS..."
find_and_copy "virtual_file_system.gd" "${TARGET_DIR}/autoload/virtual_file_system.gd"
find_and_copy "gothic_terminal.tscn" "${TARGET_DIR}/scenes/terminal/gothic_terminal.tscn"
find_and_copy "gothic_terminal.gd" "${TARGET_DIR}/scripts/terminal/gothic_terminal.gd"

echo "--> [4/5] Locating and Migrating Chamber V & Strata Sync..."
find_and_copy "ChamberV.tscn" "${TARGET_DIR}/scenes/chambers/chamber_v.tscn"
find_and_copy "ChamberV.gd" "${TARGET_DIR}/scripts/chambers/chamber_v.gd"
find_and_copy "CathedralSync.gd" "${TARGET_DIR}/core/sync/cathedral_sync.gd"
find_and_copy "ash_archive.db" "${TARGET_DIR}/strata/ash_archive.db"
find_and_copy "ash_archive.gd" "${TARGET_DIR}/core/ash_archive.gd"

echo "--> [5/5] Locating and Migrating Avatar Engine & Shaders..."
find_and_copy "CathedralAtlasBuilder.gd" "${TARGET_DIR}/systems/avatar/cathedral_atlas_builder.gd"
find_and_copy "CathedralAvatarPortrait.gd" "${TARGET_DIR}/systems/avatar/cathedral_avatar_portrait.gd"
find_and_copy "SomaticToPortraitBridge.gd" "${TARGET_DIR}/systems/avatar/somatic_to_portrait_bridge.gd"
find_and_copy "CharacterRecipe.json" "${TARGET_DIR}/data/character_recipes/character_recipe.json"
find_and_copy "cathedral_portrait_dither.gdshader" "${TARGET_DIR}/shaders/cathedral_portrait_dither.gdshader"

# File Permissions & UID Sanitization
chmod 644 "${TARGET_DIR}/strata/ash_archive.db" 2>/dev/null || true

echo "--> Sanitizing internal scene script paths & legacy UIDs..."
if [ -d "${TARGET_DIR}/scenes" ]; then
    find "${TARGET_DIR}/scenes" -type f -name "*.tscn" -exec sed -i '' \
        -e 's|res://ChamberV.gd|res://scripts/chambers/chamber_v.gd|g' \
        -e 's|res://scripts/ChamberV.gd|res://scripts/chambers/chamber_v.gd|g' \
        -e 's| uid="uid://[^"]*"||g' {} +
fi

echo "=== [CATHEDRAL ENGINE CONSOLIDATION] Dynamic Migration Complete ==="
