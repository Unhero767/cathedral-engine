#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Direct Consolidation Script (Track 1)
# Configured for Kenneth's Exact macOS Filesystem Layout
# ==============================================================================
set -euo pipefail

HOME_DIR="/Users/kennethdallmier"
TARGET_DIR="${HOME_DIR}/cathedral-engine/cathedral_engine_full_project"

# Source Repositories
SRC_BUS="${HOME_DIR}/godotmlaos"
SRC_PHYSICS="${HOME_DIR}/new-game-project"
SRC_GODOT="${HOME_DIR}/GODOT"
SRC_CATHEDRAL="${HOME_DIR}/cathedral_engine/godot_client"
SRC_AVATAR="${HOME_DIR}/cathedral_engine/cathedral_integration_pipeline/godot4_runtime"
SRC_AVATAR_ROOT="${HOME_DIR}/cathedral_engine"

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
mkdir -p "${TARGET_DIR}/addons"

copy_first_existing() {
    local dest="$1"
    shift
    for src in "$@"; do
        if [ -f "${src}" ]; then
            cp -v "${src}" "${dest}"
            return 0
        elif [ -d "${src}" ]; then
            cp -rv "${src}/." "${dest}/"
            return 0
        fi
    done
    echo "[WARNING] None of the candidate files found for: ${dest}"
}

# 2. Global Signal Bus
echo "--> [1/6] Migrating Global Signal Bus from ${SRC_BUS}..."
copy_first_existing "${TARGET_DIR}/autoload/event_bus.gd" \
    "${SRC_BUS}/autoload/event_bus.gd" \
    "${SRC_BUS}/event_bus.gd"

# 3. Bio-Semantic Physics & Soulframe
echo "--> [2/6] Migrating Bio-Semantic Physics & Soulframe from ${SRC_PHYSICS}..."
copy_first_existing "${TARGET_DIR}/core/spectral_constants.gd" \
    "${SRC_PHYSICS}/core/spectral_constants.gd" \
    "${SRC_PHYSICS}/spectral_constants.gd"

copy_first_existing "${TARGET_DIR}/core/a_field_manager.gd" \
    "${SRC_PHYSICS}/core/a_field_manager.gd" \
    "${SRC_PHYSICS}/a_field_manager.gd"

copy_first_existing "${TARGET_DIR}/core/dialetheic_buffer.gd" \
    "${SRC_PHYSICS}/core/dialetheic_buffer.gd" \
    "${SRC_PHYSICS}/dialetheic_buffer.gd"

copy_first_existing "${TARGET_DIR}/systems/metamorphic_squeeze.gd" \
    "${SRC_PHYSICS}/systems/metamorphic_squeeze.gd" \
    "${SRC_PHYSICS}/metamorphic_squeeze.gd"

copy_first_existing "${TARGET_DIR}/shaders/harmonic_scar.gdshader" \
    "${SRC_PHYSICS}/shaders/harmonic_scar.gdshader" \
    "${SRC_PHYSICS}/harmonic_scar.gdshader"

if [ -d "${SRC_PHYSICS}/systems/soulframe" ]; then
    cp -rv "${SRC_PHYSICS}/systems/soulframe/." "${TARGET_DIR}/systems/soulframe/" 2>/dev/null || true
fi

# 4. Gothic Terminal & VFS
echo "--> [3/6] Migrating Gothic Terminal & VFS from ${SRC_GODOT}..."
copy_first_existing "${TARGET_DIR}/autoload/virtual_file_system.gd" \
    "${SRC_GODOT}/autoload/virtual_file_system.gd" \
    "${SRC_BUS}/res:/autoload/virtual_file_system.gd" \
    "${SRC_GODOT}/virtual_file_system.gd"

copy_first_existing "${TARGET_DIR}/scenes/terminal/gothic_terminal.tscn" \
    "${SRC_GODOT}/scenes/terminal/gothic_terminal.tscn" \
    "${SRC_GODOT}/gothic_terminal.tscn" \
    "${SRC_GODOT}/scenes/gothic_terminal.tscn"

copy_first_existing "${TARGET_DIR}/scripts/terminal/gothic_terminal.gd" \
    "${SRC_GODOT}/scripts/terminal/gothic_terminal.gd" \
    "${SRC_GODOT}/gothic_terminal.gd" \
    "${SRC_GODOT}/scripts/gothic_terminal.gd"

# 5. Chamber V & SQLite Strata Sync
echo "--> [4/6] Migrating Chamber V & Strata Sync from ${SRC_CATHEDRAL}..."
copy_first_existing "${TARGET_DIR}/scenes/chambers/chamber_v.tscn" \
    "${SRC_CATHEDRAL}/ChamberV.tscn" \
    "${SRC_AVATAR_ROOT}/ChamberV.tscn"

copy_first_existing "${TARGET_DIR}/scripts/chambers/chamber_v.gd" \
    "${SRC_CATHEDRAL}/ChamberV.gd" \
    "${SRC_AVATAR_ROOT}/ChamberV.gd"

copy_first_existing "${TARGET_DIR}/core/sync/cathedral_sync.gd" \
    "${SRC_CATHEDRAL}/CathedralSync.gd" \
    "${SRC_AVATAR_ROOT}/CathedralSync.gd" \
    "${SRC_CATHEDRAL}/core/CathedralSync.gd"

copy_first_existing "${TARGET_DIR}/strata/ash_archive.db" \
    "${SRC_CATHEDRAL}/strata/ash_archive.db" \
    "${SRC_AVATAR_ROOT}/strata/ash_archive.db" \
    $(mdfind -onlyin "${SRC_AVATAR_ROOT}" -name "ash_archive.db" 2>/dev/null | head -n 1)

copy_first_existing "${TARGET_DIR}/core/ash_archive.gd" \
    "${SRC_CATHEDRAL}/core/ash_archive.gd" \
    "${SRC_CATHEDRAL}/ash_archive.gd" \
    "${SRC_AVATAR_ROOT}/ash_archive.gd"

# 6. Avatar Engine
echo "--> [5/6] Migrating Avatar Engine from ${SRC_AVATAR}..."
copy_first_existing "${TARGET_DIR}/systems/avatar/cathedral_atlas_builder.gd" \
    "${SRC_AVATAR}/CathedralAtlasBuilder.gd" \
    "${SRC_AVATAR_ROOT}/CathedralAtlasBuilder.gd"

copy_first_existing "${TARGET_DIR}/systems/avatar/cathedral_avatar_portrait.gd" \
    "${SRC_AVATAR}/CathedralAvatarPortrait.gd" \
    "${SRC_AVATAR_ROOT}/CathedralAvatarPortrait.gd"

copy_first_existing "${TARGET_DIR}/systems/avatar/somatic_to_portrait_bridge.gd" \
    "${SRC_AVATAR}/SomaticToPortraitBridge.gd" \
    "${SRC_AVATAR_ROOT}/SomaticToPortraitBridge.gd"

copy_first_existing "${TARGET_DIR}/data/character_recipes/character_recipe.json" \
    "${SRC_AVATAR}/CharacterRecipe.json" \
    "${SRC_AVATAR_ROOT}/CharacterRecipe.json"

copy_first_existing "${TARGET_DIR}/shaders/cathedral_portrait_dither.gdshader" \
    "${SRC_AVATAR}/cathedral_portrait_dither.gdshader" \
    "${SRC_AVATAR_ROOT}/cathedral_portrait_dither.gdshader"

# 7. Canonical project.godot Auto-Provisioning
echo "--> [6/6] Provisioning canonical project.godot..."
cat << 'EOF' > "${TARGET_DIR}/project.godot"
; Engine configuration file.
; It's best edited using the editor UI and not directly,
; but it can be edited by hand if you know what you are doing.

config_version=5

[application]

config/name="Cathedral Engine Full Project"
config/features=PackedStringArray("4.3", "GL Compatibility")
config/icon="res://icon.svg"

[autoload]

EventBus="*res://autoload/event_bus.gd"
SpectralConstants="*res://core/spectral_constants.gd"
VirtualFileSystem="*res://autoload/virtual_file_system.gd"
AshArchive="*res://core/ash_archive.gd"
AFieldManager="*res://core/a_field_manager.gd"
CathedralSync="*res://core/sync/cathedral_sync.gd"

[rendering]

renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/canvas_textures/default_texture_filter=0
