import os, sys, json, math, random
from datetime import datetime, timezone

FLUX_MAJORS = ["The Axis", "The Threshold", "The Mirror", "The Anvil", "The Prism", "The Void Core", "The Echo Tide"]
CHROMAS = ["Gold", "Sapphire", "Amethyst", "Crimson", "Teal", "Obsidian", "Rose"]
IDENTITY_VECTORS = ["Sovereign", "Architect", "Valkyrie", "Nomad", "Cipher", "Warden", "Drifter"]
REBELLIONS = ["Plasma Phase-Flip", "Structural Shear", "Axiom Fracture", "Void Inversion", "Lithic Rebirth", "Thermal Squeeze"]

def draw_ignition_card():
    r = random.random()
    if r < 0.15:
        return {"type": "Flux Major", "name": random.choice(FLUX_MAJORS), "spectrum": "Gold"}
    elif r < 0.75:
        c = random.choice(CHROMAS)
        v = random.choice(IDENTITY_VECTORS)
        return {"type": "Persona", "name": f"{c} × {v}", "spectrum": c}
    else:
        return {"type": "Rebellion", "name": random.choice(REBELLIONS), "spectrum": "Crimson"}

def run_oracle_sim(simulations=500):
    print("\n" + "="*65)
    print(" IGNITION ARCANA // DPIP MONTE CARLO SIMULATOR")
    print("="*65)
    print(f" Running {simulations} dual-vector resonance cycles...\n")

    outcomes = {"Constructive Resonance": 0, "Orthogonal Translation": 0, "Destructive Dissonance": 0}
    
    for _ in range(simulations):
        v1 = [random.uniform(-1, 1), random.uniform(-1, 1)]
        v2 = [random.uniform(-1, 1), random.uniform(-1, 1)]
        dot = v1[0]*v2[0] + v1[1]*v2[1]
        mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = math.sqrt(v2[0]**2 + v2[1]**2)
        
        cos_theta = max(-1.0, min(1.0, dot / (mag1 * mag2))) if (mag1 > 0 and mag2 > 0) else 0.0
        angle = math.degrees(math.acos(cos_theta))

        if angle < 35:
            outcomes["Constructive Resonance"] += 1
        elif angle > 145:
            outcomes["Destructive Dissonance"] += 1
        else:
            outcomes["Orthogonal Translation"] += 1

    sample_a = draw_ignition_card()
    sample_b = draw_ignition_card()
    print(" SAMPLE ARCANA DRAW:")
    print(f" [Vector A]: {sample_a['name']} ({sample_a['type']} - {sample_a['spectrum']})")
    print(f" [Vector B]: {sample_b['name']} ({sample_b['type']} - {sample_b['spectrum']})")
    print("-"*65)
    print(" DPIP INTERFERENCE DISTRIBUTION:")
    for k, v in outcomes.items():
        pct = (v / simulations) * 100
        bar = "█" * int(pct / 3)
        print(f" * {k:24s}: {v:4d} ({pct:5.1f}%) | {bar}")
    print("="*65 + "\n")

if __name__ == "__main__":
    run_oracle_sim(100)
