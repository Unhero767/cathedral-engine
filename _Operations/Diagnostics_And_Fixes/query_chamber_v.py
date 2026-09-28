import urllib.request
import urllib.parse
import json

URL = "http://localhost:5050/api/rpg/chamber?id=5"

print("================================================================================")
print(" QUERYING /api/rpg/chamber?id=5 — CHAMBER V MANIFEST")
print("================================================================================")

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "CathedralInspector/1.0"})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"[-] HTTP Query error: {e}")
