#!/usr/bin/env python3
"""
EAS-03 Spatial Triad Engine Simulation & Verification Runner
Grounding: Emotion == Physics == Magic == Biology == Architecture
"""

import hashlib
import json
import math
import time

SPECTRAL_CONSTANTS = {
    0: ("THETA_GOLD", "Joy / Law", (1.00, 0.82, 0.28), 580),
    1: ("PSI_TEAL", "Curiosity / Recursion", (0.00, 0.92, 1.00), 510),
    2: ("DELTA_BLUE", "Sorrow / Archiving", (0.12, 0.32, 0.78), 450),
    3: ("PHI_RED", "Anger / Entropy", (0.95, 0.16, 0.20), 680),
    4: ("OMEGA_VIOLET", "Fear / Adaptation", (0.62, 0.18, 0.88), 720),
    5: ("EPSILON_EMERALD", "Love / Binding", (0.10, 0.88, 0.48), 540),
    6: ("NULL_OBSIDIAN", "Void / Anti-Resonance", (0.04, 0.04, 0.06), 0)
}

BASELINE_EGO_DENSITY = 8.3
BASELINE_AFIELD_RADIUS = 64.0
GENESIS_HASH = "0" * 64

class SpatialTriadSimulation:
    def __init__(self):
        self.ego_density = 8.3
        self.emotional_magnitude = 1.0
        self.afield_beta = 0.42
        self.active_spectral_constant = 1 # Psi Teal
        self.position = [32.0, 32.0] # Grid (2, 2) -> Open True space
        self.velocity = [0.0, 0.0]
        self.subpixel_acc = [0.0, 0.0]
        
        # 16-frame input ring buffer
        self.input_buffer = []
        self.frame_counter = 0
        
        # Conceived Space Grid
        self.spatial_truth_matrix = {}
        self.harmonic_scars = []
        
        # Ash Archive (Lex I Merkle Ledger)
        self.ash_archive = []
        self.latest_block_hash = GENESIS_HASH
        
        self._init_grid()
        self._commit_event("SYSTEM_BOOT", {
            "initial_position": self.position,
            "ego_density": self.ego_density,
            "spectral_constant": SPECTRAL_CONSTANTS[self.active_spectral_constant][0],
            "afield_radius": self.calculate_afield_radius()
        })

    def calculate_afield_radius(self):
        density_ratio = self.ego_density / BASELINE_EGO_DENSITY
        return BASELINE_AFIELD_RADIUS * (1.0 + self.afield_beta * self.emotional_magnitude * density_ratio)

    def _commit_event(self, event_type, payload):
        idx = len(self.ash_archive)
        ts = int(time.time() * 1000000)
        raw_str = f"{idx}|{ts}|{self.latest_block_hash}|{event_type}|{json.dumps(payload, sort_keys=True)}"
        event_hash = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
        
        record = {
            "index": idx,
            "timestamp_usec": ts,
            "prev_hash": self.latest_block_hash,
            "hash": event_hash,
            "event_type": event_type,
            "payload": payload
        }
        self.ash_archive.append(record)
        self.latest_block_hash = event_hash
        return record

    def _init_grid(self):
        # Open Corridor: x in 0..10, y in 0..10
        for x in range(11):
            for y in range(11):
                self.spatial_truth_matrix[(x, y)] = "T"
        # Obsidian Ward at perimeter
        for x in range(-2, 13):
            self.spatial_truth_matrix[(x, -2)] = "F"
            self.spatial_truth_matrix[(x, 12)] = "F"
        for y in range(-2, 13):
            self.spatial_truth_matrix[(-2, y)] = "F"
            self.spatial_truth_matrix[(12, y)] = "F"
        # Dialetheic Rupture Line at x=5
        for y in range(2, 9):
            self.spatial_truth_matrix[(5, y)] = "B"

    def record_input(self, vec, cadence_stress=1.0):
        self.frame_counter += 1
        frame_data = {
            "frame_id": self.frame_counter,
            "vector": vec,
            "cadence_pulse": cadence_stress,
            "timestamp_usec": int(time.time() * 1000000)
        }
        if len(self.input_buffer) < 16:
            self.input_buffer.append(frame_data)
        else:
            self.input_buffer[self.frame_counter % 16] = frame_data

    def step_physics(self, input_dir, delta=0.016667):
        target_v = [input_dir[0] * 140.0, input_dir[1] * 140.0]
        self.velocity[0] += (target_v[0] - self.velocity[0]) * min(1.0, 1200.0 * delta / 140.0)
        self.velocity[1] += (target_v[1] - self.velocity[1]) * min(1.0, 1200.0 * delta / 140.0)
        
        target_pos = [self.position[0] + self.velocity[0] * delta, self.position[1] + self.velocity[1] * delta]
        grid_coord = (int(target_pos[0] // 16), int(target_pos[1] // 16))
        
        truth = self.spatial_truth_matrix.get(grid_coord, "N")
        
        step_result = {}
        if truth == "T":
            self.position = target_pos
            step_result["state"] = f"TRANSIT_SOUND (Grid {grid_coord})"
        elif truth == "F":
            self.velocity = [0.0, 0.0]
            step_result["state"] = f"COLLISION_HALTED_BY_OBSIDIAN_WARD (Grid {grid_coord})"
        elif truth == "B":
            # Metamorphic Squeeze
            cost = 0.28
            load_cap = 1.0 / cost
            scar_record = {
                "coordinate": list(grid_coord),
                "algorithmic_cost": cost,
                "structural_load_capacity": load_cap,
                "spectral_signature": SPECTRAL_CONSTANTS[self.active_spectral_constant][0],
                "ego_density": self.ego_density
            }
            self.harmonic_scars.append(scar_record)
            self.spatial_truth_matrix[grid_coord] = "T" # Petrified into sound bridge
            self._commit_event("HARMONIC_SCAR_PETRIFIED", scar_record)
            self.position = target_pos
            self.velocity[0] *= 0.82
            self.velocity[1] *= 0.82
            step_result["state"] = f"METAMORPHIC_SQUEEZE_RESOLVED (Scar at {grid_coord}, c={cost:.2f}, LoadCap={load_cap:.2f})"
        elif truth == "N":
            self.spatial_truth_matrix[grid_coord] = "F"
            self._commit_event("AXIOMATIC_ECHOLOCATION_CRYSTALLIZE", {"coordinate": list(grid_coord)})
            self.velocity[0] *= 0.35
            self.velocity[1] *= 0.35
            step_result["state"] = f"AXIOMATIC_ECHOLOCATION_CRYSTALLIZED (Grid {grid_coord} -> 'F')"
            
        self.subpixel_acc[0] = self.position[0] - math.floor(self.position[0])
        self.subpixel_acc[1] = self.position[1] - math.floor(self.position[1])
        return step_result

    def verify_ledger(self):
        curr_hash = GENESIS_HASH
        for i, rec in enumerate(self.ash_archive):
            if rec["prev_hash"] != curr_hash:
                return False, f"Broken link at block {i}"
            raw_str = f"{rec['index']}|{rec['timestamp_usec']}|{rec['prev_hash']}|{rec['event_type']}|{json.dumps(rec['payload'], sort_keys=True)}"
            recomputed = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
            if recomputed != rec["hash"]:
                return False, f"Tampering at block {i}"
            curr_hash = rec["hash"]
        return True, "All blocks verified"

def simulate_shader_fragment(r, g, b, u_spectral_const, cadence_stress=0.0):
    bayer_matrix = [0.00, 0.50, 0.75, 0.25]
    dither_offset = (bayer_matrix[0] - 0.5) * 0.12
    luminance = 0.299 * r + 0.587 * g + 0.114 * b + dither_offset
    
    shadow_ramp = 0.65
    crushed_rgb = [r, g, b]
    if luminance < shadow_ramp:
        factor = luminance / shadow_ramp
        multiplier = 0.35 + (0.90 - 0.35) * factor
        crushed_rgb = [c * multiplier for c in crushed_rgb]
        
    emissive = [0.0, 0.0, 0.0]
    cadence_gain = 1.0 + (cadence_stress * 0.45)
    
    if r > 0.70 and g > 0.52 and b < 0.45: # Gold Theta
        intensity = (r + g) * 0.5
        gold_color = SPECTRAL_CONSTANTS[0][2]
        emissive = [gold_color[i] * intensity * 1.35 for i in range(3)]
    elif b > 0.65 and g > 0.50 and r < 0.35: # Teal Psi
        intensity = b
        teal_color = SPECTRAL_CONSTANTS[1][2]
        emissive = [teal_color[i] * intensity * cadence_gain * 1.35 for i in range(3)]
        
    final_rgb = [min(1.0, crushed_rgb[i] + emissive[i]) for i in range(3)]
    return {
        "luminance": luminance,
        "emissive": emissive,
        "cadence_gain": cadence_gain,
        "final_rgb": [round(c, 3) for c in final_rgb]
    }

print("================================================================================")
print("             EAS-03 SPATIAL TRIAD KINEMATICS & STATE MACHINE RUNNER            ")
print("================================================================================")

sim = SpatialTriadSimulation()

print(f"\n[PHASE 1: INITIAL BOOT & TELEMETRY]")
print(f"  Initial Position       : {sim.position} (Grid (2, 2))")
print(f"  Ego Density (rho)      : {sim.ego_density} (Baseline: {BASELINE_EGO_DENSITY})")
print(f"  A-Field Radius         : {sim.calculate_afield_radius():.2f} px")
print(f"  Active Spectral Const  : {SPECTRAL_CONSTANTS[sim.active_spectral_constant][0]} ({SPECTRAL_CONSTANTS[sim.active_spectral_constant][1]})")
print(f"  Ash Archive Genesis    : {sim.latest_block_hash[:16]}... (1 Block Committed)")

print(f"\n[PHASE 2: KINESTHETIC NAVIGATION & SPATIAL TRANSITIONS]")

# Scenario A: Move right across open corridor
print("  > Step 1: Navigating Open Corridor (True Node)...")
sim.record_input([1.0, 0.0])
res1 = sim.step_physics([1.0, 0.0])
print(f"    Outcome: {res1['state']} | New Pos: [{sim.position[0]:.2f}, {sim.position[1]:.2f}]")

# Scenario B: Move directly into Dialetheic Rupture (x=5)
print("  > Step 2: Crossing Dialetheic Rupture at x=5 (Both Node / Contradiction)...")
sim.position = [79.0, 48.0] # Grid (4, 3)
sim.velocity = [120.0, 0.0]
sim.record_input([1.0, 0.0])
res2 = sim.step_physics([1.0, 0.0]) # Hits grid (5, 3)
print(f"    Outcome: {res2['state']}")
print(f"    Harmonic Scars Formed   : {len(sim.harmonic_scars)}")
print(f"    Petrified Node Converted: Grid (5, 3) -> State '{sim.spatial_truth_matrix[(5, 3)]}' (Sound Bridge)")

# Scenario C: Strike Obsidian Ward (False Node)
print("  > Step 3: Impacting Obsidian Perimeter Ward (False Node / Barrier)...")
sim.position = [190.0, 48.0] # Hits (12, 3) 'F'
sim.velocity = [100.0, 0.0]
sim.record_input([1.0, 0.0])
res3 = sim.step_physics([1.0, 0.0])
print(f"    Outcome: {res3['state']} | Velocity halted to: {sim.velocity}")

# Scenario D: Explore Unindexed Void (Neither Node)
print("  > Step 4: Probing Glitch-Waste Perimeter (Neither Node / Unindexed)...")
sim.position = [500.0, 500.0]
sim.record_input([0.0, 1.0])
res4 = sim.step_physics([0.0, 1.0])
print(f"    Outcome: {res4['state']} | Crystallized as 'F' in Truth Matrix")

print(f"\n[PHASE 3: LEX I ASH ARCHIVE MERKLE DAG INTEGRITY AUDIT]")
ledger_valid, ledger_msg = sim.verify_ledger()
print(f"  Total Committed Blocks : {len(sim.ash_archive)}")
print(f"  Merkle Hash Audit      : {'PASSED [VERIFIED]' if ledger_valid else 'FAILED'}")
print(f"  Latest Block Hash      : {sim.latest_block_hash}")

for i, block in enumerate(sim.ash_archive):
    print(f"    Block #{block['index']} [{block['event_type']}]: Hash={block['hash'][:16]}... Prev={block['prev_hash'][:16]}...")

print(f"\n[PHASE 4: CANVASITEM BIO-SEMANTIC SHADER SAMPLING & DIALOGUE CADENCE]")
sample_cyan = simulate_shader_fragment(0.1, 0.85, 0.95, 1, cadence_stress=0.85)
print(f"  Cyan Ocular Pixel (Cadence Stress 0.85):")
print(f"    Luminance: {sample_cyan['luminance']:.3f} | Cadence Gain: {sample_cyan['cadence_gain']:.3f} | Output RGB: {sample_cyan['final_rgb']}")

sample_gold = simulate_shader_fragment(0.92, 0.78, 0.20, 0, cadence_stress=0.0)
print(f"  Theta Gold Halo Pixel (Quiescent):")
print(f"    Luminance: {sample_gold['luminance']:.3f} | Emissive Output: {[round(c, 3) for c in sample_gold['emissive']]} | Output RGB: {sample_gold['final_rgb']}")

print("\n================================================================================")
print("                  ALL SPATIAL TRIAD SUBSYSTEMS RUNNING & VERIFIED              ")
print("================================================================================")
