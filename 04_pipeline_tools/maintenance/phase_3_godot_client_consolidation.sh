#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Phase 3: Godot 4 Client Consolidation & Path Rewriting
# Relocates scenes, scripts, shaders, archetypes, and C# systems into 03_godot_client/
# and updates internal res:// resource mappings and preloads in lockstep.
# ==============================================================================
set -euo pipefail

BASE_DIR="/users/kennethdallmier/cathedral_engine"
CLIENT_DIR="${BASE_DIR}/03_godot_client"

SCENES_DIR="${CLIENT_DIR}/scenes"
SCRIPTS_DIR="${CLIENT_DIR}/scripts"
CORE_SCRIPTS_DIR="${SCRIPTS_DIR}/core"
CSHARP_DIR="${CLIENT_DIR}/csharp"
SHADERS_DIR="${CLIENT_DIR}/shaders"
ARCHETYPES_DIR="${CLIENT_DIR}/archetypes"
SYSTEMS_DIR="${CLIENT_DIR}/systems"

echo "=== [CATHEDRAL ENGINE] Initializing Phase 3 Godot Client Consolidation ==="

mkdir -p "${SCENES_DIR}"
mkdir -p "${SCRIPTS_DIR}"
mkdir -p "${CORE_SCRIPTS_DIR}"
mkdir -p "${CSHARP_DIR}"
mkdir -p "${SHADERS_DIR}"
mkdir -p "${ARCHETYPES_DIR}"
mkdir -p "${SYSTEMS_DIR}"

safe_move() {
    local src="$1"
    local dest="$2"
    if [ -e "${src}" ] || [ -L "${src}" ]; then
        echo "--> Moving $(basename "${src}") -> ${dest}"
        mv "${src}" "${dest}/"
    fi
}

# 1. Back up project.godot and main scene
echo "[1/6] Creating safety backups of project configuration..."
cp "${BASE_DIR}/project.godot" "${BASE_DIR}/project.godot.pre_phase3_bak"

# 2. Migrate Scenes (*.tscn)
echo "[2/6] Migrating Godot Scene Files..."
for f in "${BASE_DIR}"/*.tscn; do
    [ -e "${f}" ] && safe_move "${f}" "${SCENES_DIR}"
done
if [ -d "${BASE_DIR}/scenes" ]; then
    for f in "${BASE_DIR}/scenes"/*.tscn; do
        [ -e "${f}" ] && safe_move "${f}" "${SCENES_DIR}"
    done
    rmdir "${BASE_DIR}/scenes" 2>/dev/null || true
fi

# 3. Migrate Shaders (*.gdshader, *.frag, *.uid)
echo "[3/6] Migrating Shaders..."
for f in "${BASE_DIR}"/*.gdshader* "${BASE_DIR}"/*.frag; do
    [ -e "${f}" ] && safe_move "${f}" "${SHADERS_DIR}"
done
if [ -d "${BASE_DIR}/shaders" ]; then
    for f in "${BASE_DIR}/shaders"/*; do
        [ -e "${f}" ] && safe_move "${f}" "${SHADERS_DIR}"
    done
    rmdir "${BASE_DIR}/shaders" 2>/dev/null || true
fi

# 4. Migrate GDScripts & Core scripts (*.gd, *.uid)
echo "[4/6] Migrating GDScripts..."
for f in "${BASE_DIR}"/*.gd "${BASE_DIR}"/*.gd.uid; do
    [ -e "${f}" ] && safe_move "${f}" "${SCRIPTS_DIR}"
done
if [ -d "${BASE_DIR}/core" ]; then
    for f in "${BASE_DIR}/core"/*; do
        [ -e "${f}" ] && safe_move "${f}" "${CORE_SCRIPTS_DIR}"
    done
    rmdir "${BASE_DIR}/core" 2>/dev/null || true
fi

# 5. Migrate C# Systems (*.cs)
echo "[5/6] Migrating C# Systems..."
for f in "${BASE_DIR}"/*.cs; do
    [ -e "${f}" ] && safe_move "${f}" "${CSHARP_DIR}"
done

# 6. Migrate Archetypes and Systems
echo "[6/6] Migrating Archetypes & Systems..."
if [ -d "${BASE_DIR}/archetypes" ]; then
    for f in "${BASE_DIR}/archetypes"/*; do
        [ -e "${f}" ] && safe_move "${f}" "${ARCHETYPES_DIR}"
    done
    rmdir "${BASE_DIR}/archetypes" 2>/dev/null || true
fi
if [ -d "${BASE_DIR}/systems" ]; then
    cp -rn "${BASE_DIR}/systems"/* "${SYSTEMS_DIR}/" 2>/dev/null || true
    rm -rf "${BASE_DIR}/systems" 2>/dev/null || true
fi

echo "=== [PATH REWRITING] Updating res:// path references ==="

# Update project.godot
sed -i '' 's|run/main_scene="res://CathedralAvatarDemo.tscn"|run/main_scene="res://03_godot_client/scenes/CathedralAvatarDemo.tscn"|g' "${BASE_DIR}/project.godot"

# Update CathedralAvatarDemo.tscn
if [ -f "${SCENES_DIR}/CathedralAvatarDemo.tscn" ]; then
    sed -i '' \
        -e 's|res://CathedralAvatarHarness.gd|res://03_godot_client/scripts/CathedralAvatarHarness.gd|g' \
        -e 's|res://core/SomaticToPortraitBridge.gd|res://03_godot_client/scripts/core/SomaticToPortraitBridge.gd|g' \
        -e 's|res://core/CathedralDialogueDriver.gd|res://03_godot_client/scripts/core/CathedralDialogueDriver.gd|g' \
        -e 's|res://core/CathedralAvatarDebugger.gd|res://03_godot_client/scripts/core/CathedralAvatarDebugger.gd|g' \
        -e 's|res://CathedralCharacterCreator.gd|res://03_godot_client/scripts/CathedralCharacterCreator.gd|g' \
        "${SCENES_DIR}/CathedralAvatarDemo.tscn"
fi

# Update spatial_triad_demo_scene.tscn
if [ -f "${SCENES_DIR}/spatial_triad_demo_scene.tscn" ]; then
    sed -i '' 's|res://AtlasAnimator.gd|res://03_godot_client/scripts/AtlasAnimator.gd|g' "${SCENES_DIR}/spatial_triad_demo_scene.tscn"
fi

# Update preloads in CathedralCharacterCreator.gd
if [ -f "${SCRIPTS_DIR}/CathedralCharacterCreator.gd" ]; then
    sed -i '' \
        -e 's|res://core/CathedralAtlasBuilder.gd|res://03_godot_client/scripts/core/CathedralAtlasBuilder.gd|g' \
        -e 's|res://core/CathedralSomaticEngine.gd|res://03_godot_client/scripts/core/CathedralSomaticEngine.gd|g' \
        -e 's|res://CathedralAshArchive.gd|res://03_godot_client/scripts/CathedralAshArchive.gd|g' \
        -e 's|res://archetypes/%s.json|res://03_godot_client/archetypes/%s.json|g' \
        -e 's|res://archetypes/%s.dna|res://03_godot_client/archetypes/%s.dna|g' \
        "${SCRIPTS_DIR}/CathedralCharacterCreator.gd"
fi

# Update preloads in spatial_triad scripts
if [ -f "${SCRIPTS_DIR}/spatial_triad_harness.gd" ]; then
    sed -i '' 's|res://spatial_triad_controller.gd|res://03_godot_client/scripts/spatial_triad_controller.gd|g' "${SCRIPTS_DIR}/spatial_triad_harness.gd"
fi
if [ -f "${SCRIPTS_DIR}/test_spatial_triad_unit.gd" ]; then
    sed -i '' 's|res://spatial_triad_controller.gd|res://03_godot_client/scripts/spatial_triad_controller.gd|g' "${SCRIPTS_DIR}/test_spatial_triad_unit.gd"
fi
if [ -f "${SCRIPTS_DIR}/spatial_triad_controller.gd" ]; then
    sed -i '' 's|res://cathedral_atlas_builder.gd|res://03_godot_client/scripts/core/CathedralAtlasBuilder.gd|g' "${SCRIPTS_DIR}/spatial_triad_controller.gd"
fi

# Update preloads in core/CathedralAvatarPortrait.gd
if [ -f "${CORE_SCRIPTS_DIR}/CathedralAvatarPortrait.gd" ]; then
    sed -i '' 's|res://CathedralAtlasBuilder.gd|res://03_godot_client/scripts/core/CathedralAtlasBuilder.gd|g' "${CORE_SCRIPTS_DIR}/CathedralAvatarPortrait.gd"
fi

echo "=== [CATHEDRAL ENGINE] Phase 3 Godot Client Consolidation Complete ==="
