#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Phase 2: Operations & Pipeline Consolidation
# Migrates operational scripts, patches, generators, dashboards, and releases
# into their designated numbered directories without affecting the Godot client.
# ==============================================================================
set -euo pipefail

BASE_DIR="/users/kennethdallmier/cathedral_engine"

CHAMBER_OPS_DIR="${BASE_DIR}/04_pipeline_tools/maintenance/chamber_ops"
PATCHES_DIR="${BASE_DIR}/04_pipeline_tools/maintenance/patches"
ATLAS_DIR="${BASE_DIR}/04_pipeline_tools/atlas_compiler"
COMFY_DIR="${BASE_DIR}/04_pipeline_tools/comfyui_bridge"
DASHBOARDS_DIR="${BASE_DIR}/05_web_interface/dashboards"
RELEASES_DIR="${BASE_DIR}/07_dist_releases/1.0.0_master"

echo "=== [CATHEDRAL ENGINE] Initializing Phase 2 Consolidation ==="
mkdir -p "${CHAMBER_OPS_DIR}"
mkdir -p "${PATCHES_DIR}"
mkdir -p "${ATLAS_DIR}"
mkdir -p "${COMFY_DIR}"
mkdir -p "${DASHBOARDS_DIR}"
mkdir -p "${RELEASES_DIR}"

safe_move() {
    local src="$1"
    local dest="$2"
    if [ -e "${BASE_DIR}/${src}" ] || [ -L "${BASE_DIR}/${src}" ]; then
        echo "--> Moving ${src} -> ${dest}"
        mv "${BASE_DIR}/${src}" "${dest}/"
    fi
}

echo "[1/5] Migrating Chamber Operations & Navigation Scripts..."
# Movement scripts
for f in move_to_*.py; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${CHAMBER_OPS_DIR}"
done
safe_move "move_and_examine_pillar_alpha.py" "${CHAMBER_OPS_DIR}"

# Inspection & query scripts
for f in inspect_chamber_*.py inspect_active_*.py query_chamber_*.py; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${CHAMBER_OPS_DIR}"
done
safe_move "inspect_ledger_state.py" "${CHAMBER_OPS_DIR}"
safe_move "get_active_state.py" "${CHAMBER_OPS_DIR}"
safe_move "display_final_telemetry.py" "${CHAMBER_OPS_DIR}"

# Transition, tune & traverse scripts
for f in transition_to_*.py tune_*.py traverse_*.py; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${CHAMBER_OPS_DIR}"
done

# Interaction & chamber execution scripts
for f in interact_*.py examine_*.py inscribe_*.py; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${CHAMBER_OPS_DIR}"
done
safe_move "interface_archive_terminal.py" "${CHAMBER_OPS_DIR}"
safe_move "regulate_nitrogen_pressure.py" "${CHAMBER_OPS_DIR}"
safe_move "simulate_chamber_v_patrol.py" "${CHAMBER_OPS_DIR}"
safe_move "synthesize_chamber_artifact.py" "${CHAMBER_OPS_DIR}"
safe_move "ensure_server_and_chamber_v.py" "${CHAMBER_OPS_DIR}"
safe_move "engage_ash_terminal.py" "${CHAMBER_OPS_DIR}"
safe_move "engage_transcendence_oculus.py" "${CHAMBER_OPS_DIR}"
safe_move "persist_victory.py" "${CHAMBER_OPS_DIR}"

echo "[2/5] Migrating Patches, Bugfixes & Repairs..."
for f in patch_*.py fix_*.py fix_*.sh repair_*.py; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${PATCHES_DIR}"
done
safe_move "reset_engine.py" "${PATCHES_DIR}"
safe_move "safe_writes.py" "${PATCHES_DIR}"
safe_move "prove_safe.py" "${PATCHES_DIR}"
safe_move "consolidate_engine.sh" "${PATCHES_DIR}"
safe_move "consolidate_engine_direct.sh" "${PATCHES_DIR}"
safe_move "consolidate_engine_v2.sh" "${PATCHES_DIR}"
safe_move "consolidate_engine_v3.sh" "${PATCHES_DIR}"

echo "[3/5] Migrating Pipeline & Generative Tools..."
safe_move "cathedral_atlas_generator.py" "${ATLAS_DIR}"
safe_move "generate_master_atlas.py" "${ATLAS_DIR}"
safe_move "generate_7_archetypes.py" "${ATLAS_DIR}"
safe_move "generate_titan.py" "${ATLAS_DIR}"
safe_move "cathedral_dna_exporter.py" "${ATLAS_DIR}"
safe_move "update_atlas_animator.py" "${ATLAS_DIR}"
safe_move "cathedral_codex_generator.py" "${ATLAS_DIR}"
safe_move "cathedral_local_generator.py" "${ATLAS_DIR}"

safe_move "comfy_bridge.py" "${COMFY_DIR}"
safe_move "run_comfy.py" "${COMFY_DIR}"
safe_move "run_comfy_workflow.py" "${COMFY_DIR}"
safe_move "generate_workflow.py" "${COMFY_DIR}"
safe_move "workflow_api.json" "${COMFY_DIR}"
safe_move "fine_tune_cathedral_lora.py" "${COMFY_DIR}"
safe_move "train_standalone.py" "${COMFY_DIR}"

echo "[4/5] Migrating Web Dashboards & HTML Studios..."
safe_move "cathedral_ultimate_creator.html" "${DASHBOARDS_DIR}"
safe_move "cathedral_masterpiece_studio.html" "${DASHBOARDS_DIR}"
safe_move "cathedral_avatar_engine.html" "${DASHBOARDS_DIR}"
safe_move "cathedral_dnd_creator.html" "${DASHBOARDS_DIR}"
safe_move "lillith.html" "${DASHBOARDS_DIR}"
for f in mlaos_prime_master_civilization_engine*.html; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${DASHBOARDS_DIR}"
done

echo "[5/5] Migrating Distribution Archives & Packages..."
for f in cathedral_engine_1.0.0-master-turnkey_*.tar.gz cathedral_engine_*.zip cc_omega_15_recipes.zip; do
    [ -e "${BASE_DIR}/${f}" ] && safe_move "${f}" "${RELEASES_DIR}"
done
safe_move "release_manifest.sha256.pdf" "${RELEASES_DIR}"

echo "=== [CATHEDRAL ENGINE] Phase 2 Consolidation Complete ==="
