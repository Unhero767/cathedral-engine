#!/usr/bin/env python3
import os
import sys
import json

REPO_ROOT = "/users/kennethdallmier/cathedral_engine"
sys.path.insert(0, os.path.join(REPO_ROOT, "02_engine_core", "logic_engines"))
sys.path.insert(0, os.path.join(REPO_ROOT, "02_engine_core"))

from game_loop_engine import GameLoopEngine, CHAMBER_MANIFESTS

print("=" * 70)
print("CATHEDRAL-ENGINE // CHAMBER I -> II PROGRESSION SIMULATION")
print("=" * 70)

engine = GameLoopEngine(base_dir=REPO_ROOT)

# 1. Boot session in Chamber I
print("\n[Stage 1: Initializing Protagonist in Chamber I: The Lithic Threshold]")
state = engine.start_new_game("Kiri Vespera", "Void Walker")
p = state["player"]
c1 = CHAMBER_MANIFESTS[1]

print(f"  * Entity   : {p['name']} [{p['archetype']}]")
print(f"  * Chamber  : {c1['name']}")
print(f"  * Position : ({p['x']}, {p['y']})")
print(f"  * Carrier  : {c1['carrier_hz']:.1f} Hz [{c1['spectral_dominant']}]")
print(f"  * Ambient  : {c1['temperature_k']:.2f} K | Pressure: {c1['pressure_bar']:.2f} bar")

# 2. Navigate across Chamber I
print("\n[Stage 2: Navigating Exploration Grid toward Threshold Portal (7, 7)]")
steps = [(3, 3), (5, 5), (7, 7)]
for x, y in steps:
    res = engine.player_move(x, y)
    print(f"  -> Stepped to ({x}, {y}) | Log: {res['action_log'][-1]}")

# 3. Verify Chamber II State
print("\n[Stage 3: Verifying Chamber II State & Cryogenic Heat Sink Telemetry]")
final_state = engine.get_full_game_state()
p2 = final_state["player"]
c2 = CHAMBER_MANIFESTS[p2["chamber"]]

temp_c = c2["temperature_k"] - 273.15
print(f"  * Inscribed Chamber: {c2['name']}")
print(f"  * Central Node     : ({p2['x']}, {p2['y']})")
print(f"  * Carrier Resonance: {c2['carrier_hz']:.2f} Hz [{c2['spectral_dominant']}]")
print(f"  * Thermal State    : {c2['temperature_k']:.2f} K ({temp_c:.2f} °C) [Liquid Nitrogen Equilibrium]")
print(f"  * Nitrogen Pressure: {c2['pressure_bar']:.2f} bar [Regulated Target Achieved]")
print(f"  * Cryo Flow Rate   : {c2['cryo_flow_rate_l_min']:.1f} L/min")
print(f"  * Player Attunement: {p2['emotional_state']} (Spectrum: {p2['spectrum']})")

# 4. Render Chamber II 8x8 Spatial Grid
print("\n[Stage 4: Chamber II Spatial Map Grid (8x8)]")
grid_w, grid_h = 8, 8
grid = [[" . " for _ in range(grid_w)] for _ in range(grid_h)]
grid[p2["y"]][p2["x"]] = " K "  # Kiri Vespera at (4, 4)
grid[2][2] = "[N]"  # Nitrogen Pressure Manifold
grid[5][5] = "[H]"  # Somatic Heat Sink Core
grid[7][7] = "[P]"  # Portal to Chamber III

print("   " + " ".join(f"{x}" for x in range(grid_w)))
print("  +" + "---" * grid_w + "+")
for y, row in enumerate(grid):
    print(f"{y:2d}|" + "".join(row) + "|")
print("  +" + "---" * grid_w + "+")
print("  Legend: [K] Kiri Vespera (4, 4) | [N] Nitrogen Manifold | [H] Somatic Heat Sink | [P] Chamber III Portal")

print("\n" + "=" * 70)
print("PROGRESSION SIMULATION COMPLETE: CHAMBER II ACTIVE [T]")
print("=" * 70)
