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
print(" CHAMBER II :: REGULATING NITROGEN PRESSURE")
print("==================================================")

params = {
    "target_uid": "cryo_sink_01",
    "x": 4,
    "y": 4,
    "action": "REGULATE_PRESSURE",
    "target_pressure_bar": 2.1
}

try:
    print("[*] Dispatching regulation command -> Target Pressure: 2.1 bar...")
    res = get("interact", params)
    print("\nInteraction Response:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print("[-] Interaction failed:", e)

print("\n==================================================")
print(" UPDATED TELEMETRY & STRATA STATUS")
print("==================================================")
try:
    # Query state/telemetry to confirm manifold stabilization
    state = get("state")
    player = state.get("player", {})
    print(f"Chamber Position: ({player.get('x', 4)}, {player.get('y', 4)})")
    print(f"Active Spectrum:  {player.get('spectrum', 'Teal')}")
    
    logs = state.get("action_log", [])
    if logs:
        print("\nRecent Strata Action Log:")
        for log in logs[-3:]:
            print(f"  • {log}")
except Exception as e:
    print("[-] State verification error:", e)
