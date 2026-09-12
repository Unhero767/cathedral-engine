import sys
import requests

API_BASE = "http://127.0.0.1:8000"
node_id = sys.argv[1] if len(sys.argv) > 1 else "aurelia-12"
load = float(sys.argv[2]) if len(sys.argv) > 2 else 8.42

res = requests.post(f"{API_BASE}/node/sync", json={
    "instance_id": node_id,
    "mqi_score": 94.7,
    "a_field_temperature_k": 308.5,
    "current_flux": 2.14,
    "active_spectrum": "BRONZE_OBSIDIAN",
    "active_paradox_load": load
})
print(f"=== NODE SYNC EXECUTED ({node_id}) ===")
print(res.json())
