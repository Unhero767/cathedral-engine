#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Lithic Strain Accumulator Simulation
# File: simulate_lithic_strain.py
# ==============================================================================

import numpy as np
import json
import os

def simulate_material_stress():
    print("[CATHE_LITHIC] Initializing state-persistence material stress matrix...")
    
    # Simulate spatial grid nodes across a structural beam (X-axis coordinates in meters)
    nodes = np.linspace(0.0, 10.0, 11)
    
    # Applied mechanical stress history profile (MegaPascals) featuring a localized stress concentration point
    base_stress = 15.0  # MPa nominal load
    stress_concentration = 45.0 * np.exp(-((nodes - 6.5)**2) / 0.5) # Stress peak at x = 6.5m
    total_stress = base_stress + stress_concentration
    
    # Material threshold for permanent crystal phase shift / micro-fracture inscription (MPa)
    yield_threshold_mpa = 35.0
    
    material_strata = []
    for idx, (coord, stress) in enumerate(zip(nodes, total_stress)):
        phase_shift_fraction = max(0.0, (stress - yield_threshold_mpa) / yield_threshold_mpa) if stress > yield_threshold_mpa else 0.0
        remediation_triggered = phase_shift_fraction > 0.2
        
        record = {
            "node_id": idx,
            "position_m": float(coord),
            "peak_stress_mpa": float(stress),
            "crystal_phase_shift_density": float(phase_shift_fraction),
            "lithic_memory_status": "LOCKED_TRAUMA" if phase_shift_fraction > 0 else "NOMINAL",
            "autonomous_remediation_active": bool(remediation_triggered)
        }
        material_strata.append(record)
        print(f"[CATHE_LITHIC] Node {idx:2d} @ {coord:4.1f}m | Stress: {stress:5.1f} MPa | Phase Shift: {phase_shift_fraction:.2f} | Remediation: {remediation_triggered}")

    output_path = "strata/lithic_stress_ledger.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(material_strata, f, indent=4)
        
    print(f"[CATHE_LITHIC] State-persistence simulation recorded. Ledger updated at {output_path}.")

if __name__ == "__main__":
    simulate_material_stress()
