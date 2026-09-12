import requests

API_BASE = "http://127.0.0.1:8000"
print("=== CONNECTING TO SSE TELEMETRY STREAM (/stream/state) ===")
try:
    response = requests.get(f"{API_BASE}/stream/state", stream=True, timeout=5)
    for line in response.iter_lines():
        if line:
            print("Pushed Event:", line.decode('utf-8'))
            break
except Exception as e:
    print("Stream connected or closed:", e)
