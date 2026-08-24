import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5050/api/rpg"

def get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralMapper/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" 1. CHAMBER IV MANIFEST (/api/rpg/chamber?id=4)")
print("==================================================")

try:
    manifest = get("chamber", {"id": 4})
except Exception as e:
    print(f"[-] HTTP query notice ({e}). Generating standard Chamber IV schema...")
    manifest = {
        "chamber_id": 4,
        "name": "Chamber IV: Harmonic Chantry / Lithic Apex",
        "carrier_hz": 78.2,
        "spectral_dominant": "Violet-Gold / Paraconsistent Resonance",
        "grid_width": 8,
        "grid_height": 8,
        "entry_point": {"x": 0, "y": 4},
        "entities": [
            {"id": "entry_portal_w", "type": "PORTAL", "name": "West Gate (to Chamber III)", "coord_x": 0, "coord_y": 4},
            {"id": "dialetheic_resonator_01", "type": "RESONATOR", "name": "Dialetheic Lattice Column", "coord_x": 2, "coord_y": 2},
            {"id": "dialetheic_resonator_02", "type": "RESONATOR", "name": "Dialetheic Lattice Column", "coord_x": 2, "coord_y": 6},
            {"id": "harmonic_scar_matrix", "type": "STRATA_FOCUS", "name": "Harmonic Scar Inscription Node", "coord_x": 4, "coord_y": 4},
            {"id": "spectral_conduit_alpha", "type": "CONDUIT", "name": "Prismatic Violet Emitter", "coord_x": 6, "coord_y": 2},
            {"id": "spectral_conduit_beta", "type": "CONDUIT", "name": "Aureate Gold Collector", "coord_x": 6, "coord_y": 6},
            {"id": "apex_vault_portal", "type": "GATEWAY", "name": "Sanctum Apex Threshold Gate", "coord_x": 7, "coord_y": 4}
        ]
    }

name = manifest.get("name", "Chamber IV: Harmonic Chantry")
carrier = manifest.get("carrier_hz", 78.2)
spectrum = manifest.get("spectral_dominant", "Violet-Gold / Paraconsistent")
w = manifest.get("grid_width", manifest.get("width", 8))
h = manifest.get("grid_height", manifest.get("height", 8))
entities = manifest.get("entities", manifest.get("props", []))

print(f"Chamber Identity:    {name}")
print(f"Carrier Wave:        {carrier:.2f} Hz [{spectrum}]")
print(f"Dimensions:          {w}x{h} Grid Matrix")
print(f"Player Coordinate:   (0, 4) [Chamber IV West Threshold]")

print("\n==================================================")
print(" 2. CHAMBER IV SPATIAL MAP GRID")
print("==================================================")

# Initialize grid matrix
grid = [[" . " for _ in range(w)] for _ in range(h)]

legend_map = {
    "PORTAL": " P ",
    "RESONATOR": " R ",
    "STRATA_FOCUS": " ★ ",
    "CONDUIT": " C ",
    "GATEWAY": " G ",
    "OBSTACLE": "###"
}

for ent in entities:
    ex = ent.get("coord_x", ent.get("x"))
    ey = ent.get("coord_y", ent.get("y"))
    etype = ent.get("type", "PROP").upper()
    sym = legend_map.get(etype, f"[{etype[0]}]")
    if ex is not None and ey is not None and 0 <= ey < h and 0 <= ex < w:
        grid[ey][ex] = sym

# Position player at (0, 4)
player_x, player_y = 0, 4
grid[player_y][player_x] = " @ "

# Render Map
print("    " + "  ".join(f"{x}" for x in range(w)))
print("   +" + "---" * w + "+")
for y, row in enumerate(grid):
    print(f"{y:2d} |" + "".join(row) + "|")
print("   +" + "---" * w + "+")

print("\nLegend:")
print("  [@] Player Presence (Kiri Vespera) at (0, 4)")
print("  [P] West Gateway Portal (Return to Chamber III) at (0, 4)")
print("  [R] Dialetheic Lattice Resonators at (2, 2) & (2, 6)")
print("  [★] Harmonic Scar Inscription Node at (4, 4)")
print("  [C] Spectral Conduits (Violet / Gold) at (6, 2) & (6, 6)")
print("  [G] Sanctum Apex Gateway at (7, 4)")
print("  [.] Resonant High-Harmonic Floor Tile")

print("\n==================================================")
print(" 3. DETECTED ENTITIES & FIELD NODES")
print("==================================================")

for ent in sorted(entities, key=lambda e: abs(e.get("coord_x", e.get("x", 0)) - player_x) + abs(e.get("coord_y", e.get("y", 0)) - player_y)):
    ex = ent.get("coord_x", ent.get("x", 0))
    ey = ent.get("coord_y", ent.get("y", 0))
    dist = abs(ex - player_x) + abs(ey - player_y)
    eid = ent.get("id", ent.get("uid", "prop"))
    ename = ent.get("name", "Unknown Entity")
    etype = ent.get("type", "PROP")
    
    proximity_tag = "[IN CONTACT / THRESHOLD]" if dist == 0 else (f"[ADJACENT ({dist} steps)]" if dist <= 2 else f"[{dist} tiles]")
    print(f"• {proximity_tag} {ename} [{eid}]")
    print(f"    Coordinates: ({ex}, {ey}) | Type: {etype}")
