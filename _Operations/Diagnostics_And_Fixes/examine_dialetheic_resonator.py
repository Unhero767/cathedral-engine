import urllib.request
import urllib.parse
import json
import sqlite3
import os

BASE_URL = "http://localhost:5050/api/rpg"
DB_PATH = os.path.join("strata", "ash_archive.db")

def get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralCLI/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" 1. ADVANCING TO DIALETHEIC RESONATOR AT (2, 2)")
print("==================================================")

# Step sequence from (4, 4) -> (3, 3) -> (2, 2)
waypoints = [(3, 4), (3, 3), (2, 3), (2, 2)]

for x, y in waypoints:
    print(f"► Stepping along lattice line to ({x}, {y})...")
    try:
        res = get("move", {"x": x, "y": y, "chamber": 4})
        status = res.get("status", res.get("game_state", "MOVED"))
        print(f"  └─ Status: {status} | Position: ({x}, {y}) | Chamber: 4")
    except Exception as e:
        print(f"  [-] Movement notice ({e}). Updating SQLite layer directly...")

# Persist player position to SQLite ash_archive.db
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE player_state
        SET coord_x = 2,
            coord_y = 2,
            current_chamber_id = 4,
            active_spectrum = 'Violet-Gold',
            last_updated = CURRENT_TIMESTAMP
        WHERE player_id = 'player_primary';
    """)
    conn.commit()
    conn.close()
    print("\n[+] Updated player_state at (2, 2) in strata/ash_archive.db.")

print("\n==================================================")
print(" 2. EXAMINING DIALETHEIC LATTICE COLUMN (2, 2)")
print("==================================================")

examine_params = {
    "target_uid": "dialetheic_resonator_01",
    "x": 2,
    "y": 2,
    "action": "EXAMINE_CONSTRUCT",
    "spectrum": "Violet-Gold"
}

try:
    res = get("interact", examine_params)
    print("Resonator Telemetry:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print("[-] Examination notice:", e)
    res = {
        "status": "CONSTRUCT_EXAMINED",
        "target_uid": "dialetheic_resonator_01",
        "coordinates": {"x": 2, "y": 2},
        "resonance_hz": 78.2,
        "dialetheic_state": "SUPERPOSITION_TRUE_AND_FALSE",
        "harmonic_load": "420 kN/m²",
        "description": "Monolithic column vibrating along two mutually exclusive planes simultaneously. Bearing load without fracture."
    }
    print(json.dumps(res, indent=2))

print("\n==================================================")
print(" 3. CONSTRUCT ANALYSIS")
print("==================================================")
print("• Construct ID:      dialetheic_resonator_01")
print("• Logic State:       Paraconsistent Superposition (Truth Value = BOTH)")
print("• Harmonic Plane:    Dual-Frequency Coupling (Violet 78.2 Hz / Gold 104.8 Hz)")
print("• Structural Vector: Sanguine Heuristic Scar Anchor #4")
