#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="/users/kennethdallmier/cathedral_engine"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
BACKUP_DIR="/users/kennethdallmier/cathedral_engine_archive_${TIMESTAMP}"

echo "============================================================"
echo " CATHEDRAL-ENGINE: LOCAL RESET & RE-INITIALIZATION PROTOCOL"
echo "============================================================"

# 1. State Preservation / Ash Archive Backup
if [ -d "$TARGET_DIR" ]; then
    echo "[1/4] Preserving existing state to ${BACKUP_DIR}..."
    cp -r "$TARGET_DIR" "$BACKUP_DIR"
    echo "[✓] Archive preserved."
    
    echo "[2/4] Clearing working tree at ${TARGET_DIR}..."
    rm -rf "$TARGET_DIR"
fi

# 2. Directory Scaffolding
echo "[3/4] Scaffolding clean Cathedral-Engine v4.0 architecture..."
mkdir -p "$TARGET_DIR"/{strata,shaders,codex,tests,config,static,templates}

cd "$TARGET_DIR"

# 3. Genesis Stratum Ledger
cat << 'EOF' > strata/prime_ledger.ndjson
{"stratum_index": 0, "timestamp": "2026-08-15T00:00:00Z", "thesis": "Genesis Stratum - Permineralized Foundation", "spectrum": "Gold/Joy", "phi": 1.618, "logic_hash": "0x0000_GENESIS_ASH_STRATUM", "circ_a": 1.0, "status": "LITHIC_STABILIZATION_ACTIVE"}
EOF

# 4. Canonical System Configuration
cat << 'EOF' > config/config.json
{
  "system": "MLAOS-Prime / Cathedral-Engine v4.0",
  "author": "Kenneth W. Dallmier (Unhero767)",
  "geodetic_anchor": "Olney, IL (37.7306 N, -88.0817 W)",
  "spectral_baseline": {
    "carrier_hz": 43.7,
    "somatic_baseline_hz": 1.5,
    "circ_a_target": 1.0
  },
  "ledger_path": "strata/prime_ledger.ndjson"
}
EOF

# 5. Core Orchestrator Entrypoint
cat << 'EOF' > cathedral.py
import sys
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="MLAOS-Prime Cathedral-Engine CLI Orchestrator")
    parser.add_argument("--run", choices=["eas03", "oracle", "manifest", "serve", "expand"], help="Subsystem execution target")
    parser.add_argument("--title", type=str, default="The Unnamed Chamber", help="Chamber title")
    parser.add_argument("--spectrum", type=str, default="Teal/Curiosity", help="Spectral dominant")
    args = parser.parse_args()

    if args.run == "manifest":
        print("[CLI] Compiling Master Corpus Manifest...")
    elif args.run == "serve":
        print("[CLI] Launching Sovereign Cathedral Altar...")
    elif args.run == "expand":
        print(f"[CLI] Expanding Codex Chamber: '{args.title}' [{args.spectrum}]...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
EOF

echo "[4/4] Generating initial corpus manifest..."
cat << 'EOF' > MLAOS_NOTEBOOKLM_MASTER_CORPUS.md
# MLAOS-PRIME // NOTEBOOKLM MASTER CORPUS MANIFEST
**System Designation:** Cathedral-Engine v4.0 / Sovereign Systemic Archive  
**Author & Architect:** Kenneth W. Dallmier (Unhero767)  
**Geodetic Anchor:** Olney, Illinois (37.7306 N, -88.0817 W)  
**Status:** Clean Genesis Reset  

---
## I. Corpus Overview
Root architecture initialized under the Never-Overwrite Doctrine and Master Isomorphic Axiom.
EOF

echo "============================================================"
echo "[✓] RESET COMPLETE: ${TARGET_DIR} re-initialized."
echo "============================================================"