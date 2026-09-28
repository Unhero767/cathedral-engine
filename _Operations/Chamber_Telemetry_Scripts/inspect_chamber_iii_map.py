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
print(" 1. CHAMBER III MANIFEST (/api/rpg/chamber?id=3)")
print("==================================================")

try:
    manifest = get("chamber", {"id": 3})
except Exception as e:
    print(f"[-] HTTP Query notice: {e}. Generating default manifest schema.")
    manifest = {
        "chamber_id": 3,
        "name": "Chamber III: Pneumatic Vault",
        "carrier_hz": 65.4,
        "spectral_dominant": "Blue / Sorrow",
        "grid_width": 8,
        "grid_height": 8,
        "entry_point": {"x": 0, "y": 4},
        "entities": [
            {"id": "entry_portal_w", "type": "PORTAL", "name": "West Gate (to Chamber II)", "coord_x": 0, "coord_y": 4},
            {"id": "aerostatic_manifold_01", "type": "MANIFOLD", "name": "Pneumatic Column Regulator", "coord_x": 2, "coord_y": 4},
            {"id": "pressure_exhaust_north", "type": "EXHAUST", "name": "Ventilation Flue Alpha", "coord_x": 3, "coord_y": 1},
            {"id": "pressure_exhaust_south", "type": "EXHAUST", "name": "Ventilation Flue Beta", "coord_x": 3, "coord_y": 7},
            {"id": "terminal_strata_blue", "type": "TERMINAL", "name": "Aerostatic Archive Conduit", "coord_x": 5, "coord_y": 4},
            {"id": "east_vault_barrier", "type": "GATEWAY", "name": "Chamber IV Threshold Gate", "coord_x": 7, "coord_y": 4}
        ]
    }

name = manifest.get("name", "Chamber III: Pneumatic Vault")
carrier = manifest.get("carrier_hz", 65.4)
spectrum = manifest.get("spectral_dominant", "Blue / Sorrow")
w = manifest.get("grid_width", manifest.get("width", 8))
h = manifest.get("grid_height", manifest.get("height", 8))
entities = manifest.get("entities", manifest.get("props", []))

print(f"Chamber Identity:    {name}")
print(f"Carrier Wave:        {carrier:.2f} Hz [{spectrum}]")
print(f"Dimensions:          {w}x{h} Grid Matrix")
print(f"Active Player Node:  (0, 4)")

print("\n==================================================")
print(" 2. SPATIAL MAP GRID & OCCUPANCY")
print("==================================================")

# Initialize blank grid
grid = [[" . " for _ in range(w)] for _ in range(h)]

# Place entities on grid
legend_map = {
    "PORTAL": " P ",
    "MANIFOLD": " M ",
    "EXHAUST": " V ",
    "TERMINAL": " T ",
    "GATEWAY": " G ",
    "OBSTACLE": "###"
}

for ent in entities:
    ex = ent.get("coord_x", ent.get("x"))
    ey = ent.get("coord_y", ent.get("y"))
    etype = ent.get("type", "PROP").upper()
    symbol = legend_map.get(etype, f"[{etype[0]}]")
    
    if ex is not None and ey is not None and 0 <= ey < h and 0 <= ex < w:
        grid[ey][ex] = symbol

# Mark current player position
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
print("  [P] West Gateway Portal (Return to Chamber II)")
print("  [M] Aerostatic Manifold Column Regulator at (2, 4)")
print("  [V] Pneumatic Exhaust Flues at (3, 1) & (3, 7)")
print("  [T] Aerostatic Archive Conduit Terminal at (5, 4)")
print("  [G] Chamber IV Gateway Barrier at (7, 4)")
print("  [.] Resonant Blue Strata Tile")

print("\n==================================================")
print(" 3. NEARBY PROPS & ENTITIES RELATIVE TO (0, 4)")
print("==================================================")

for ent in sorted(entities, key=lambda e: abs(e.get("coord_x", e.get("x", 0)) - player_x) + abs(e.get("coord_y", e.get("y", 0)) - player_y)):
    ex = ent.get("coord_x", ent.get("x", 0))
    ey = ent.get("coord_y", ent.get("y", 0))
    dist = abs(ex - player_x) + abs(ey - player_y)
    eid = ent.get("id", ent.get("uid", "prop"))
    ename = ent.get("name", "Unknown Prop")
    etype = ent.get("type", "PROP")
    
    proximity_tag = "[ADJACENT / REACHABLE]" if dist <= 2 else f"[{dist} tiles away]"
    print(f"• {proximity_tag} {ename} ({eid})")
    print(f"    Position: ({ex}, {ey}) | Type: {etype}")
