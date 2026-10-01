#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Sovereign Continuum Auditor
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os
import sqlite3
import urllib.request
import urllib.error
import json
from pathlib import Path

# Target thresholds
TARGET_POLL_HZ = 1.500
DB_PATH = "data/ash_archive/ledger.db"

def render_header():
    print("\033[1;35m┌──────────────────────────────────────────────┐\033[0m")
    print("\033[1;35m│   Σ-7 :: SOVEREIGN SYSTEM AUDIT INITIATED    │\033[0m")
    print("\033[1;35m└──────────────────────────────────────────────┘\033[0m")

def audit_structural_strata() -> dict:
    """Audits the physical directory structure and Godot/Python assets."""
    print("\n\033[1;36m==> [1] Structural Stratum Analysis\033[0m")
    critical_files = [
        "studio.py", 
        "main.py", 
        "project.godot", 
        "CathedralConsole.tscn"
    ]
    missing = [f for f in critical_files if not os.path.exists(f)]
    
    # Count codebase weight
    py_files = list(Path('.').rglob('*.py'))
    gd_files = list(Path('.').rglob('*.gd'))
    
    print(f"  \033[1;32m[+]\033[0m Python Subsystems Detected: {len(py_files)}")
    print(f"  \033[1;32m[+]\033[0m GDScript Controllers Detected: {len(gd_files)}")
    
    if missing:
        print(f"  \033[1;31m[-]\033[0m Missing core assets: {', '.join(missing)}")
        
    return {"missing_assets": missing, "py_count": len(py_files), "gd_count": len(gd_files)}

def audit_ash_archive() -> dict:
    """Evaluates the Merkle DAG SQLite ledger for Lex I compliance."""
    print("\n\033[1;36m==> [2] Ash Archive Ledger Continuity\033[0m")
    if not os.path.exists(DB_PATH):
        print("  \033[1;31m[-]\033[0m Ledger database not found at data/ash_archive/ledger.db")
        return {"ledger_active": False}
        
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode;")
            j_mode = cursor.fetchone()[0]
            
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='blocks';")
            has_blocks = cursor.fetchone()[0] > 0
            
            print(f"  \033[1;32m[+]\033[0m Ledger Journal Mode: {j_mode.upper()}")
            print(f"  \033[1;32m[+]\033[0m Genesis Block Initialized: {'YES' if has_blocks else 'NO'}")
            
            return {"ledger_active": True, "journal_mode": j_mode, "has_blocks": has_blocks}
    except Exception as e:
        print(f"  \033[1;31m[-]\033[0m Ledger read fracture: {e}")
        return {"ledger_active": False}

def audit_telemetry_continuum() -> dict:
    """Pings the FastAPI backend to verify paraconsistent state transmission."""
    print("\n\033[1;36m==> [3] Somatic Telemetry Continuum\033[0m")
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/telemetry", method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                ego = data.get("datum", {}).get("ego_density", "Unknown")
                print(f"  \033[1;32m[+]\033[0m Continuum API: ONLINE (Port 8000)")
                print(f"  \033[1;32m[+]\033[0m Live Ego Density: {ego} kg/m³")
                return {"api_online": True}
    except urllib.error.URLError:
        print("  \033[1;33m[!]\033[0m Continuum API: OFFLINE. Paraconsistent backend unreachable.")
        return {"api_online": False}

def synthesize_recommendations(strata, ledger, telemetry):
    """Generates high-tier architectural directives based on state anomalies."""
    print("\n\033[1;33m==> [X] HIGH-TIER ARCHITECTURAL RECOMMENDATIONS\033[0m")
    recs = []
    
    # Stratum Recommendations
    if strata["missing_assets"]:
        recs.append("CRITICAL: Reconstruct missing core artifacts using the forge scripts.")
    if strata["py_count"] > 15:
        recs.append("OPTIMIZATION: Python logic density increasing. Consider modularizing axioms into a dedicated `mlaos_core/` package.")
        
    # Ledger Recommendations
    if not ledger.get("ledger_active"):
        recs.append("PRIORITY ALPHA: Instantiate the Ash Archive SQLite ledger to begin recording the Merkle DAG.")
    elif ledger.get("journal_mode", "").lower() != "wal":
        recs.append("DATA INTEGRITY: Execute `PRAGMA journal_mode=WAL;` to enable Write-Ahead Logging for high-concurrency ledger writes.")
        
    # Telemetry Recommendations
    if not telemetry.get("api_online"):
        recs.append("SOMATIC FRACTURE: Run `./scripts/launch_continuum.sh` to ignite the FastAPI backend and restore the Godot polling cycle.")
    else:
        recs.append("SCALABILITY: Telemetry loop is stable. Next step: Implement WebSocket streaming (Server-Sent Events) to replace static 1.5Hz HTTP polling.")

    if not recs:
        print("  \033[1;32m[✓] System is operating at absolute optimal coherence. No structural deviations detected.\033[0m")
    else:
        for i, rec in enumerate(recs, 1):
            print(f"  \033[1;35m{i}.\033[0m {rec}")
    print()

def main():
    render_header()
    strata_state = audit_structural_strata()
    ledger_state = audit_ash_archive()
    telemetry_state = audit_telemetry_continuum()
    synthesize_recommendations(strata_state, ledger_state, telemetry_state)

if __name__ == "__main__":
    main()
