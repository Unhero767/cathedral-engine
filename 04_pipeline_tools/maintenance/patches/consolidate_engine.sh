#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Master Consolidation Script (Track 1)
# Target: /Users/kennethdallmier/cathedral-engine/cathedral_engine_full_project
# ==============================================================================
set -euo pipefail

BASE_DIR="/Users/kennethdallmier/cathedral-engine"
TARGET_DIR="${BASE_DIR}/cathedral_engine_full_project"

echo "=== [CATHEDRAL ENGINE CONSOLIDATION] Initializing Migration ==="

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

copy_file() {
    local src="$1"
    local dest="$2"
    if [ -f "${src}" ]; then
        cp -v "${src}" "${dest}"
    elif [ -d "${src}" ]; then
        cp -rv "${src}" "${dest}"
    else
        echo "[WARNING] Source not found: ${src}"
    fi
}

# 2. Global Signal Bus
SRC_BUS="${BASE_DIR}/godotmlaos"
echo "--> [1/5] Migrating Global Signal Bus..."
copy_file "${SRC_BUS}/autoload/event_bus.gd" "${TARGET_DIR}/autoload/event_bus.gd"

# 3. Bio-Semantic Physics & Soulframe
SRC_PHYSICS="${BASE_DIR}/new-game-project"
echo "--> [2/5] Migrating Bio-Semantic Physics & Soulframe..."
copy_file "${SRC_PHYSICS}/core/spectral_constants.gd" "${TARGET_DIR}/core/spectral_constants.gd"
copy_file "${SRC_PHYSICS}/core/a_field_manager.gd" "${TARGET_DIR}/core/a_field_manager.gd"
copy_file "${SRC_PHYSICS}/core/dialetheic_buffer.gd" "${TARGET_DIR}/core/dialetheic_buffer.gd"
copy_file "${SRC_PHYSICS}/systems/metamorphic_squeeze.gd" "${TARGET_DIR}/systems/metamorphic_squeeze.gd"
if [ -d "${SRC_PHYSICS}/systems/soulframe" ]; then
    cp -rv "${SRC_PHYSICS}/systems/soulframe/"* "${TARGET_DIR}/systems/soulframe/"
fi
copy_file "${SRC_PHYSICS}/shaders/harmonic_scar.gdshader" "${TARGET_DIR}/shaders/harmonic_scar.gdshader"

# 4. Gothic Terminal & VFS
SRC_GODOT="${BASE_DIR}/GODOT"
echo "--> [3/5] Migrating Gothic Terminal & VFS..."
copy_file "${SRC_GODOT}/autoload/virtual_file_system.gd" "${TARGET_DIR}/autoload/virtual_file_system.gd"
copy_file "${SRC_GODOT}/scenes/terminal/gothic_terminal.tscn" "${TARGET_DIR}/scenes/terminal/gothic_terminal.tscn"
copy_file "${SRC_GODOT}/scripts/terminal/gothic_terminal.gd" "${TARGET_DIR}/scripts/terminal/gothic_terminal.gd"

# 5. Chamber V & SQLite Sync
SRC_CATHEDRAL="${BASE_DIR}/CathedralProject"
if [ ! -d "${SRC_CATHEDRAL}" ]; then
    SRC_CATHEDRAL="${BASE_DIR}/the-cathedral"
fi
echo "--> [4/5] Migrating Chamber V & Strata Sync from ${SRC_CATHEDRAL}..."
copy_file "${SRC_CATHEDRAL}/ChamberV.tscn" "${TARGET_DIR}/scenes/chambers/chamber_v.tscn"
copy_file "${SRC_CATHEDRAL}/ChamberV.gd" "${TARGET_DIR}/scripts/chambers/chamber_v.gd"
copy_file "${SRC_CATHEDRAL}/CathedralSync.gd" "${TARGET_DIR}/core/sync/cathedral_sync.gd"
copy_file "${SRC_CATHEDRAL}/strata/ash_archive.db" "${TARGET_DIR}/strata/ash_archive.db"
if [ -f "${SRC_CATHEDRAL}/core/ash_archive.gd" ]; then
    copy_file "${SRC_CATHEDRAL}/core/ash_archive.gd" "${TARGET_DIR}/core/ash_archive.gd"
fi

# 6. Avatar Engine (Explicit snake_case Normalization)
SRC_AVATAR="${BASE_DIR}/cathedral_engine"
echo "--> [5/5] Migrating Avatar Engine from ${SRC_AVATAR}..."
copy_file "${SRC_AVATAR}/CathedralAtlasBuilder.gd" "${TARGET_DIR}/systems/avatar/cathedral_atlas_builder.gd"
copy_file "${SRC_AVATAR}/CathedralAvatarPortrait.gd" "${TARGET_DIR}/systems/avatar/cathedral_avatar_portrait.gd"
copy_file "${SRC_AVTHAR}/SomaticToPortraitBridge.gd" "${TARGET_DIR}/systems/avatar/somatic_to_portrait_bridge.gd" 2>/dev/null || true
copy_file "${SRC_AVATAR}/CharacterRecipe.json" "${TARGET_DIR}/data/character_recipes/character_recipe.json"
copy_file "${SRC_AVATAR}/cathedral_portrait_dither.gdshader" "${TARGET_DIR}/shaders/cathedral_portrait_dither.gdshader"

# 7. File Permissions & UID Sanitization
chmod 644 "${TARGET_DIR}/strata/ash_archive.db" 2>/dev/null || true

echo "--> Sanitizing internal scene script paths & legacy UIDs..."
find "${TARGET_DIR}/scenes" -type f -name "*.tscn" -exec sed -i '' \
    -e 's|res://ChamberV.gd|res://scripts/chambers/chamber_v.gd|g' \
    -e 's|res://scripts/ChamberV.gd|res://scripts/chambers/chamber_v.gd|g' \
    -e 's| uid="uid://[^"]*"||g' {} +

echo "=== [CATHEDRAL ENGINE CONSOLIDATION] Migration Complete ==="
