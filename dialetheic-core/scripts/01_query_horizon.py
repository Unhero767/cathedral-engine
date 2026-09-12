import sys
import os
import requests

API_BASE = "http://127.0.0.1:8000"
key = sys.argv[1] if len(sys.argv) > 1 else "mlaos.outer_choir.mythos.syntax_of_the_unborn"

res = requests.get(f"{API_BASE}/query?key={key}")
print(f"=== ONTOLOGICAL HORIZON QUERY ({key}) ===")
print(res.json())
