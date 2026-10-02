import urllib.request
import json
import time

url = "http://localhost:8000/telemetry"

batch = [
    {
        "tier": "STORY",
        "payload": {
            "chapter": "IV",
            "resonance": "Gold Joy",
            "content": "The golden altar breathes light across the lower vault, casting long geometric shadows."
        }
    },
    {
        "tier": "BP",
        "payload": {
            "atomKey": "sanctuary:door",
            "bp": "T",
            "sigma": "PROVEN",
            "stability": 0.96,
            "contradiction": 0.0
        }
    },
    {
        "tier": "STORY",
        "payload": {
            "chapter": "IV",
            "resonance": "Blue Sorrow",
            "content": "A sudden thermal drop fractures the western masonry, unearthing forgotten strata."
        }
    },
    {
        "tier": "BP",
        "payload": {
            "atomKey": "wall:northern",
            "bp": "B",
            "sigma": "INCONSISTENT",
            "stability": 0.74,
            "contradiction": 1.0,
            "harmonicScar": "Crystallized Vault Fracture"
        }
    }
]

print("[Godot Adapter] Initiating live telemetry simulation batch...")
for item in batch:
    req = urllib.request.Request(
        url,
        data=json.dumps(item).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"-> Emitted Tier [{item["tier"]}] | Assigned ID: {res.get("id")}")
    except Exception as e:
        print(f"-> Telemetry emission failed: {e}")
    time.sleep(0.75)

print("[Godot Adapter] Batch transmission complete.")
