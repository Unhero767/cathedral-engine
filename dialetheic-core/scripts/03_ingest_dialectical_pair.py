import sys
import requests

API_BASE = "http://127.0.0.1:8000"
claim = sys.argv[1] if len(sys.argv) > 1 else "Every chamber is wholly filled with resonant stone."
counter = sys.argv[2] if len(sys.argv) > 2 else "Every chamber is wholly empty of stone."
verse_id = sys.argv[3] if len(sys.argv) > 3 else "CLI-PAIR-01"

res = requests.post(f"{API_BASE}/ingest", json={
    "verse_id": verse_id,
    "claim": claim,
    "counter_claim": counter
})
print("=== DIALECTICAL PAIR INGESTION RESULT ===")
print(res.json())
