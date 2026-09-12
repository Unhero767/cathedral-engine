#!/usr/bin/env bash
# ==============================================================================
# Cathedral Engine - Phase 4: Sub-Repository & Lore Consolidation
# 1. Migrates lore (chambers & codices) into 01_Lore_and_Codices/
# 2. Migrates documentation & research reports into 08_docs_research/
# 3. Isolates all nested sub-repositories into Archives/Repositories/legacy_snapshots/
# ==============================================================================
set -euo pipefail

BASE_DIR="/users/kennethdallmier/cathedral_engine"

LORE_DIR="${BASE_DIR}/01_Lore_and_Codices"
CHAMBERS_DIR="${LORE_DIR}/chambers"
CODEX_DIR="${LORE_DIR}/codex"

DOCS_DIR="${BASE_DIR}/08_docs_research"
SPECS_DIR="${DOCS_DIR}/specs"
REPORTS_DIR="${DOCS_DIR}/reports"

LEGACY_DIR="${BASE_DIR}/Archives/Repositories/legacy_snapshots"

echo "=== [CATHEDRAL ENGINE] Initializing Phase 4 Repository Isolation ==="

mkdir -p "${CHAMBERS_DIR}"
mkdir -p "${CODEX_DIR}"
mkdir -p "${SPECS_DIR}"
mkdir -p "${REPORTS_DIR}"
mkdir -p "${LEGACY_DIR}"
touch "${LEGACY_DIR}/.gdignore"

safe_move() {
    local src="$1"
    local dest="$2"
    if [ -e "${BASE_DIR}/${src}" ] || [ -L "${BASE_DIR}/${src}" ]; then
        echo "--> Moving ${src} -> ${dest}"
        mv "${BASE_DIR}/${src}" "${dest}/"
    fi
}

echo "[1/3] Populating 01_Lore_and_Codices..."
if [ -d "${BASE_DIR}/expanded_chambers" ]; then
    cp -rn "${BASE_DIR}/expanded_chambers"/* "${CHAMBERS_DIR}/" 2>/dev/null || true
    rm -rf "${BASE_DIR}/expanded_chambers" 2>/dev/null || true
fi

if [ -d "${BASE_DIR}/codex" ]; then
    cp -rn "${BASE_DIR}/codex"/* "${CODEX_DIR}/" 2>/dev/null || true
    rm -rf "${BASE_DIR}/codex" 2>/dev/null || true
fi

echo "[2/3] Populating 08_docs_research..."
safe_move "Comprehensive Research Report_ Anatomy-Driven Character Customization Engine Architecture.pdf" "${REPORTS_DIR}"
safe_move "codex_master_report.txt" "${REPORTS_DIR}"
safe_move "MLAOS-SPEC-GAME-ASSET-DOMAINS-v1.0.0.md" "${SPECS_DIR}"
safe_move "corpus_manifest.json" "${SPECS_DIR}"

echo "[3/3] Isolating Nested Sub-Repositories & Parallel Snapshots..."
REPOS_TO_ISOLATE=(
    "the-cathedral"
    "godot_project"
    "godotmlaos"
    "mlaosp-sovereign-repository"
    "cathedral-engine"
    "cathedral_engine_master"
    "cathedral_engine_distribution"
    "cathedral_engine_distribution 2"
    "CathedralEngine"
    "CathedralProject"
    "Character Creation"
    "godot_client"
    "new-game-project"
    "mongo_project"
    "my-projects"
    "thearchonivist"
    "cathedral_integration_pipeline"
    "screensaber"
    "screensaver"
    "stitch"
    "stitch_deterministic_execution_kernel"
    "mlaos-emotional-physics"
    "mlaos_park"
    "biological_shield"
    "scripts1"
    "strata1"
)

for repo in "${REPOS_TO_ISOLATE[@]}"; do
    safe_move "${repo}" "${LEGACY_DIR}"
done

echo "=== [CATHEDRAL ENGINE] Phase 4 Isolation Complete ==="
