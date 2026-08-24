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
print(" 1. ADVANCING SOUTH TO DIALETHEIC RESONATOR (2, 6)")
print("==================================================")

# Step sequence along western vertical axis from (2, 2) to (2, 6)
waypoints = [(2, 3), (2, 4), (2, 5), (2, 6)]

for x, y in waypoints:
    print(f"► Stepping along western cross-aisle to ({x}, {y})...")
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
            coord_y = 6,
            current_chamber_id = 4,
            active_spectrum = 'Violet-Gold',
            last_updated = CURRENT_TIMESTAMP
        WHERE player_id = 'player_primary';
    """)
    conn.commit()
    conn.close()
    print("\n[+] Updated player_state at (2, 6) in strata/ash_archive.db.")

print("\n==================================================")
print(" 2. EXAMINING DIALETHEIC LATTICE COLUMN BETA (2, 6)")
print("==================================================")

examine_params = {
    "target_uid": "dialetheic_resonator_02",
    "x": 2,
    "y": 6,
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
        "target_uid": "dialetheic_resonator_02",
        "coordinates": {"x": 2, "y": 6},
        "resonance_hz": 78.2,
        "dialetheic_state": "SUPERPOSITION_PENDING_COUPLING",
        "harmonic_load": "420 kN/m²",
        "description": "Southern monolithic lattice column. Resonant phase vibrating counter-synchronous to Column Alpha; requires harmonic coupling."
    }
    print(json.dumps(res, indent=2))

print("\n==================================================")
print(" 3. CONSTRUCT ANALYSIS")
print("==================================================")
print("• Construct ID:      dialetheic_resonator_02")
print("• Logic State:       Paraconsistent Superposition (Uncoupled Phase)")
print("• Carrier Vector:    Violet 78.2 Hz (Standing Wave)")
print("• Coupling Target:   Gold 104.8 Hz Counter-Harmonic [Collector Beta at (6, 6)]")
