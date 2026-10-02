import requests

API_BASE = "http://127.0.0.1:8000"
res = requests.post(f"{API_BASE}/codex/ingest/book2")
print("=== BOOK II INGESTION EXECUTED ===")
print(res.json())
