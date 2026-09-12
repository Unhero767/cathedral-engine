#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Absolute Path Master Consolidation Script (Track 3)
# Target: /Users/kennethdallmier/cathedral-engine/cathedral_engine_full_project
# ==============================================================================
set -euo pipefail

HOME_DIR="/Users/kennethdallmier"
TARGET_DIR="${HOME_DIR}/cathedral-engine/cathedral_engine_full_project"

echo "=== [CATHEDRAL ENGINE CONSOLIDATION] Initializing Absolute Path Migration ==="

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

safe_copy() {
    local src="$1"
    local dest="$2"
    if [ -f "${src}" ]; then
        cp -v "${src}" "${dest}"
    elif [ -d "${src}" ]; then
        cp -rv "${src}" "${dest}"
    else
        echo "[WARNING] Source path not found: ${src}"
    fi
}

# 2. Global Signal Bus
echo "--> [1/5] Migrating Global Signal Bus..."
safe_copy "${HOME_DIR}/godotmlaos/autoload/event_bus.gd" "${TARGET_DIR}/autoload/event_bus.gd"

# 3. Bio-Semantic Physics & Soulframe (checking alternative paths if needed)
echo "--> [2/5] Migrating Bio-Semantic Physics & Soulframe..."
# Checking standard locations under home or cathedral_engine projects
safe_copy "${HOME_DIR}/cathedral_engine/core/spectral_constants.gd" "${TARGET_DIR}/core/spectral_constants.gd"
safe_copy "${HOME_DIR}/cathedral_engine/core/a_field_manager.gd" "${TARGET_DIR}/core/a_field_manager.gd"
safe_copy "${HOME_DIR}/cathedral_engine/core/dialetheic_buffer.gd" "${TARGET_DIR}/core/dialetheic_buffer.gd"
safe_copy "${HOME_DIR}/cathedral_engine/systems/metamorphic_squeeze.gd" "${TARGET_DIR}/systems/metamorphic_squeeze.gd"
safe_copy "${HOME_DIR}/cathedral_engine/shaders/harmonic_scar.gdshader" "${TARGET_DIR}/shaders/harmonic_scar.gdshader"

# 4. Gothic Terminal & VFS
echo "--> [3/5] Migrating Gothic Terminal & VFS..."
safe_copy "${HOME_DIR}/cathedral_engine/autoload/virtual_file_system.gd" "${TARGET_DIR}/autoload/virtual_file_system.gd"
safe_copy "${HOME_DIR}/cathedral_engine/scenes/terminal/gothic_terminal.tscn" "${TARGET_DIR}/scenes/terminal/gothic_terminal.tscn"
safe_copy "${HOME_DIR}/cathedral_engine/scripts/terminal/gothic_terminal.gd" "${TARGET_DIR}/scripts/terminal/gothic_terminal.gd"

# 5. Chamber V & SQLite Sync (from ~/the-cathedral)
echo "--> [4/5] Migrating Chamber V & Strata Sync..."
safe_copy "${HOME_DIR}/the-cathedral/godot_client/ChamberV.tscn" "${TARGET_DIR}/scenes/chambers/chamber_v.tscn"
safe_copy "${HOME_DIR}/the-cathedral/godot_client/ChamberV.gd" "${TARGET_DIR}/scripts/chambers/chamber_v.gd"
safe_copy "${HOME_DIR}/the-cathedral/CathedralSync.gd" "${TARGET_DIR}/core/sync/cathedral_sync.gd"
safe_copy "${HOME_DIR}/the-cathedral/strata/ash_archive.db" "${TARGET_DIR}/strata/ash_archive.db"
safe_copy "${HOME_DIR}/the-cathedral/core/ash_archive.gd" "${TARGET_DIR}/core/ash_archive.gd"

# 6. Avatar Engine & Shaders (from ~/cathedral_engine)
echo "--> [5/5] Migrating Avatar Engine & Shaders..."
safe_copy "${HOME_DIR}/cathedral_engine/CathedralAtlasBuilder.gd" "${TARGET_DIR}/systems/avatar/cathedral_atlas_builder.gd"
safe_copy "${HOME_DIR}/cathedral_engine/CathedralAvatarPortrait.gd" "${TARGET_DIR}/systems/avatar/cathedral_avatar_portrait.gd"
safe_copy "${HOME_DIR}/cathedral_engine/SomaticToPortraitBridge.gd" "${TARGET_DIR}/systems/avatar/somatic_to_portrait_bridge.gd"
safe_copy "${HOME_DIR}/cathedral_engine/CharacterRecipe.json" "${TARGET_DIR}/data/character_recipes/character_recipe.json"
safe_copy "${HOME_DIR}/cathedral_engine/cathedral_portrait_dither.gdshader" "${TARGET_DIR}/shaders/cathedral_portrait_dither.gdshader"

# File Permissions & UID Sanitization
chmod 644 "${TARGET_DIR}/strata/ash_archive.db" 2>/dev/null || true

echo "--> Sanitizing internal scene script paths & legacy UIDs..."
if [ -d "${TARGET_DIR}/scenes" ]; then
    find "${TARGET_DIR}/scenes" -type f -name "*.tscn" -exec sed -i '' \
        -e 's|res://ChamberV.gd|res://scripts/chambers/chamber_v.gd|g' \
        -e 's|res://scripts/ChamberV.gd|res://scripts/chambers/chamber_v.gd|g' \
        -e 's| uid="uid://[^"]*"||g' {} +
fi

echo "=== [CATHEDRAL ENGINE CONSOLIDATION] Absolute Path Migration Complete ==="
