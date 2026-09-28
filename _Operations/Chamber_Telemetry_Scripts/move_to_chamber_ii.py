import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5050/api/rpg"

def get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralCLI/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" 1. MOVING PLAYER TO CHAMBER II (4, 4)")
print("==================================================")
try:
    move_res = get("move", {"x": 4, "y": 4, "chamber": 2})
    print("Move Endpoint Response:")
    print(json.dumps(move_res, indent=2))
except Exception as e:
    print("[-] Move request error:", e)

print("\n==================================================")
print(" 2. VERIFYING ACTIVE RPG ENGINE STATE")
print("==================================================")
try:
    state_res = get("state")
    player = state_res.get("player", {})
    print(f"Current Mode:    {state_res.get('game_state', state_res.get('state', 'UNKNOWN'))}")
    print(f"Current Chamber: {player.get('chamber', player.get('current_chamber_id', '?'))}")
    print(f"Coordinates:     ({player.get('x', player.get('coord_x', '?'))}, {player.get('y', player.get('coord_y', '?'))})")
    print(f"Player Vitality: HP: {player.get('hp', '?')} | AP: {player.get('ap', '?')}")
    print(f"Active Spectrum: {player.get('spectrum', player.get('active_spectrum', '?'))}")
    print("Inventory Relics:")
    inv = player.get("inventory", {})
    if isinstance(inv, str):
        try: inv = json.loads(inv)
        except: pass
    for item_id, item_data in inv.items():
        name = item_data.get("name", item_id) if isinstance(item_data, dict) else item_id
        print(f"  • [{item_id}] {name}")
except Exception as e:
    print("[-] State verification error:", e)
