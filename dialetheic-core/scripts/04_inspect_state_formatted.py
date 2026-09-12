import requests
import json

API_BASE = "http://127.0.0.1:8000"
res = requests.get(f"{API_BASE}/state")
print("=== FORMATTED CATHEDRAL STATE ===")
print(json.dumps(res.json(), indent=2))
