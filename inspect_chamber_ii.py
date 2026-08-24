import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5050"

def get_json(path, params=None):
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralInspector/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" 1. CODEX ARCHIVE MANIFEST (/api/codex)")
print("==================================================")
try:
    codex_data = get_json("/api/codex")
    print(f"Status:      {codex_data.get('status')}")
    print(f"Total Books: {codex_data.get('book_count', len(codex_data.get('books', [])))}")
    print(f"Carrier Hz:  {codex_data.get('carrier_hz', 43.7)} Hz")
    
    # Filter or display Prime Foundations / Somatic entries
    books = codex_data.get("books", [])
    somatic_books = [b for b in books if any(k in str(b).lower() for k in ["somatic", "chamber ii", "ii.", "cryo"])]
    if somatic_books:
        print("\nRelevant Codex References:")
        for b in somatic_books[:3]:
            print(f"  • {b}")
except Exception as e:
    print("[-] Failed to query /api/codex:", e)

print("\n==================================================")
print(" 2. CHAMBER II MANIFEST (/api/rpg/chamber?id=2)")
print("==================================================")
try:
    chamber_data = get_json("/api/rpg/chamber", {"id": 2})
    print(json.dumps(chamber_data, indent=2))
    
    # Render ASCII Spatial Grid if grid or layout exists
    grid_w = chamber_data.get("grid_width", chamber_data.get("width", 8))
    grid_h = chamber_data.get("grid_height", chamber_data.get("height", 8))
    entry_x = chamber_data.get("entry_x", 4)
    entry_y = chamber_data.get("entry_y", 4)
    entities = chamber_data.get("entities", chamber_data.get("props", []))
    
    print("\n==================================================")
    print(f" 3. CHAMBER II SPATIAL MAP GRID ({grid_w}x{grid_h})")
    print("==================================================")
    print(f"Entry Node: ({entry_x}, {entry_y}) | Spectrum: Teal / Curiosity")
    
    grid = [[" . " for _ in range(grid_w)] for _ in range(grid_h)]
    
    # Mark entry point
    if 0 <= entry_y < grid_h and 0 <= entry_x < grid_w:
        grid[entry_y][entry_x] = " E "
        
    # Mark entities / interactables
    for ent in entities:
        ex = ent.get("x", ent.get("coord_x"))
        ey = ent.get("y", ent.get("coord_y"))
        etype = ent.get("type", ent.get("name", "O"))[0].upper()
        if ex is not None and ey is not None and 0 <= ey < grid_h and 0 <= ex < grid_w:
            grid[ey][ex] = f"[{etype}]"
            
    print("\n    " + "  ".join(f"{x}" for x in range(grid_w)))
    print("   +" + "---" * grid_w + "+")
    for y, row in enumerate(grid):
        print(f"{y:2d} |" + "".join(row) + "|")
    print("   +" + "---" * grid_w + "+")
    print("\nLegend: [E] Entry Portal | [N] Nitrogen Sink / NPC | [.] Resonant Floor Tile")

except Exception as e:
    print("[-] Failed to query /api/rpg/chamber:", e)
