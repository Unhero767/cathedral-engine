import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5050/api/rpg"

def get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralInspector/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("================================================================================")
print(" 1. CHAMBER V MANIFEST & SPECTRAL PARAMETERS (/api/rpg/chamber?id=5)")
print("================================================================================")

try:
    manifest = get("chamber", {"id": 5})
except Exception as e:
    print(f"[-] HTTP Query notice ({e}). Generating canonical Chamber V schema...")
    manifest = {
        "chamber_id": 5,
        "name": "Chamber V: Sanctum Apex / Core Monad",
        "carrier_hz": 130.81,
        "spectral_dominant": "Gold-Obsidian / Revelatory Null Matrix",
        "grid_width": 8,
        "grid_height": 8,
        "entry_point": {"x": 0, "y": 4},
        "resonance_specs": {
            "harmonic_mode": "OCTAVE_OCTET_CONVERGENCE",
            "fundamental_carrier_hz": 130.81,
            "spectral_flux": "AUREATE_OBSIDIAN_EQUILIBRIUM",
            "dialetheic_tolerance": "UNBOUNDED",
            "dPhi_dt_threshold": 1.618
        },
        "entities": [
            {"id": "entry_portal_w", "type": "PORTAL", "name": "West Portal (to Chamber IV)", "coord_x": 0, "coord_y": 4},
            {"id": "monad_somatic_anchor_n", "type": "ANCHOR", "name": "Somatic Pillar Alpha", "coord_x": 2, "coord_y": 1},
            {"id": "monad_somatic_anchor_s", "type": "ANCHOR", "name": "Somatic Pillar Beta", "coord_x": 2, "coord_y": 7},
            {"id": "core_monad_altar", "type": "CORE_ALTAR", "name": "Axiomatic Monad Matrix", "coord_x": 4, "coord_y": 4},
            {"id": "ash_stratum_repository", "type": "TERMINAL", "name": "Ash Stratum Deep Terminal", "coord_x": 6, "coord_y": 4},
            {"id": "transcendence_oculus", "type": "GATEWAY", "name": "Transcendence Oculus (Codex Gateway)", "coord_x": 7, "coord_y": 4}
        ]
    }

name = manifest.get("name", "Chamber V: Sanctum Apex / Core Monad")
carrier = manifest.get("carrier_hz", 130.81)
spectrum = manifest.get("spectral_dominant", "Gold-Obsidian / Revelatory Null")
w = manifest.get("grid_width", manifest.get("width", 8))
h = manifest.get("grid_height", manifest.get("height", 8))
specs = manifest.get("resonance_specs", {})
entities = manifest.get("entities", manifest.get("props", []))

print(f"• Chamber Designation:  {name}")
print(f"• Carrier Frequency:    {carrier:.2f} Hz [C3 Harmonic Octave]")
print(f"• Spectral Dominant:    {spectrum}")
print(f"• Convergence Mode:     {specs.get('harmonic_mode', 'OCTAVE_OCTET_CONVERGENCE')}")
print(f"• Dialetheic Limit:     {specs.get('dialetheic_tolerance', 'UNBOUNDED')}")
print(f"• dPhi/dt Threshold:    {specs.get('dPhi_dt_threshold', 1.618)} (Golden Spiral Intensity)")
print(f"• Chamber Dimensions:   {w}x{h} Grid Matrix")

print("\n================================================================================")
print(" 2. CHAMBER V SPATIAL MAP GRID")
print("================================================================================")

grid = [[" . " for _ in range(w)] for _ in range(h)]

legend_map = {
    "PORTAL": " P ",
    "ANCHOR": " A ",
    "CORE_ALTAR": " Ω ",
    "TERMINAL": " T ",
    "GATEWAY": " O ",
    "OBSTACLE": "###"
}

for ent in entities:
    ex = ent.get("coord_x", ent.get("x"))
    ey = ent.get("coord_y", ent.get("y"))
    etype = ent.get("type", "PROP").upper()
    sym = legend_map.get(etype, f"[{etype[0]}]")
    if ex is not None and ey is not None and 0 <= ey < h and 0 <= ex < w:
        grid[ey][ex] = sym

# Entry point marker
grid[4][0] = " P "

print("    " + "  ".join(f"{x}" for x in range(w)))
print("   +" + "---" * w + "+")
for y, row in enumerate(grid):
    print(f"{y:2d} |" + "".join(row) + "|")
print("   +" + "---" * w + "+")

print("\nLegend:")
print("  [P] West Entry Portal from Chamber IV at (0, 4)")
print("  [A] Somatic Anchor Pillars at (2, 1) & (2, 7)")
print("  [Ω] Core Monad Altar (Axiomatic Inscription Center) at (4, 4)")
print("  [T] Ash Stratum Deep Terminal at (6, 4)")
print("  [O] Transcendence Oculus (Codex Gateway) at (7, 4)")
print("  [.] Sanctum Gold-Obsidian Ground Strata Tile")

print("\n================================================================================")
print(" 3. CONSTRUCT MATRIX RELATIVE TO ENTRY (0, 4)")
print("================================================================================")

for ent in sorted(entities, key=lambda e: abs(e.get("coord_x", e.get("x", 0)) - 0) + abs(e.get("coord_y", e.get("y", 0)) - 4)):
    ex = ent.get("coord_x", ent.get("x", 0))
    ey = ent.get("coord_y", ent.get("y", 0))
    dist = abs(ex - 0) + abs(ey - 4)
    eid = ent.get("id", ent.get("uid", "prop"))
    ename = ent.get("name", "Unknown Entity")
    etype = ent.get("type", "PROP")
    
    status_tag = "[ENTRY VECTOR]" if dist == 0 else f"[{dist} tiles from entry]"
    print(f"• {status_tag} {ename} ({eid})")
    print(f"    Coordinates: ({ex}, {ey}) | Type: {etype}")
