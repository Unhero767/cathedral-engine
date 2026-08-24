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

print("==================================================")
print(" 1. SCANNING CHAMBER II ENTITIES NEAR (4, 4)")
print("==================================================")
try:
    chamber_manifest = get("chamber", {"id": 2})
    entities = chamber_manifest.get("entities", chamber_manifest.get("props", chamber_manifest.get("interactables", [])))
    print(f"Chamber: {chamber_manifest.get('name', 'Chamber II: Somatic Foundation')}")
    print(f"Carrier Frequency: {chamber_manifest.get('carrier_hz', 52.8)} Hz | Spectral Resonance: Teal")
    
    player_x, player_y = 4, 4
    nearby = []
    
    print("\nEntities Manifest:")
    for ent in entities:
        ex = ent.get("x", ent.get("coord_x", 0))
        ey = ent.get("y", ent.get("coord_y", 0))
        dist = abs(ex - player_x) + abs(ey - player_y)
        ent["manhattan_distance"] = dist
        name = ent.get("name", ent.get("id", "Unknown Construct"))
        etype = ent.get("type", "interactable")
        print(f"  • [{etype.upper()}] {name} at ({ex}, {ey}) -> Dist: {dist} tiles")
        if dist <= 1:
            nearby.append(ent)
            
    print(f"\nFound {len(nearby)} interactable entity/entities adjacent to ({player_x}, {player_y}).")

except Exception as e:
    print("[-] Failed to retrieve Chamber II manifest:", e)
    nearby = []

print("\n==================================================")
print(" 2. EXECUTING /api/rpg/interact ON TARGET")
print("==================================================")
# Target closest entity, or default to cryogenic regulator construct
target_uid = nearby[0].get("uid", nearby[0].get("id", "cryo_sink_01")) if nearby else "cryo_sink_01"

try:
    print(f"[*] Interacting with target entity: [{target_uid}]...")
    interact_res = get("interact", {
        "target_uid": target_uid,
        "x": 4,
        "y": 4,
        "action": "EXAMINE_SOMATIC_REGULATOR"
    })
    print("Interaction Response:")
    print(json.dumps(interact_res, indent=2))
except Exception as e:
    print("[-] /api/rpg/interact request error:", e)

print("\n==================================================")
print(" 3. ACTIVE RPG ACTION LOG & STRATA FEEDBACK")
print("==================================================")
try:
    state_res = get("state")
    logs = state_res.get("action_log", [])
    if logs:
        print("Recent Logs:")
        for l in logs[-4:]:
            print(f"  • {l}")
    else:
        print("Engine State:", json.dumps(state_res.get("player", {}), indent=2))
except Exception as e:
    print("[-] State check error:", e)
