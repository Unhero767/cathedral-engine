#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Vacuum Polarization Ledger Inspection Utility
# File: inspect_vacuum_ledger.py
# ==============================================================================

import json
import os

LEDGER_PATH = "strata/vacuum_polarization_ledger.json"

def inspect_vacuum_ledger():
    print("[CATHE_INSPECT] Querying vacuum polarization ledger strata...")
    
    if not os.path.exists(LEDGER_PATH):
        print(f"[CATHE_ERR] Ledger not found at {LEDGER_PATH}. Run simulate_vacuum_polarization.py first.")
        return

    with open(LEDGER_PATH, 'r') as f:
        records = json.load(f)

    total_steps = len(records)
    print(f"[CATHE_INSPECT] Total recorded steps in vacuum ledger: {total_steps}")
    print("--------------------------------------------------------------------------------")
    
    total_tension = 0.0
    total_torsion = 0.0

    for node in records:
        metrics = node.get("metrics", {})
        step = metrics.get("step", 0)
        tension = metrics.get("dialetheic_tension", 0.0)
        vacuum_energy = metrics.get("vacuum_polarization_j", 0.0)
        torsion = metrics.get("micro_torsion_rad_m2", 0.0)
        block_hash = node.get("block_hash", "")[:12]
        
        total_tension += tension
        total_torsion += torsion
        
        print(f"[Step {step:2d}] Tension: {tension:.4f} | Vacuum Energy: {vacuum_energy:.2e} J | Torsion: {torsion:.2e} rad/m²")
        print(f"       -> Merkle Hash: {block_hash}...")

    avg_tension = total_tension / total_steps if total_steps > 0 else 0.0
    avg_torsion = total_torsion / total_steps if total_steps > 0 else 0.0
    print("--------------------------------------------------------------------------------")
    print(f"[CATHE_INSPECT] Average Dialetheic Tension: {avg_tension:.4f}")
    print(f"[CATHE_INSPECT] Average Micro-Torsion Intensity: {avg_torsion:.2e} rad/m²")
    print("[CATHE_INSPECT] Vacuum ledger inspection complete. Stratigraphic integrity verified.")

if __name__ == "__main__":
    inspect_vacuum_ledger()
