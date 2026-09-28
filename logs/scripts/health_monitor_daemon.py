import json
import os
import sys
import urllib.request
import urllib.error

LEDGERS = [
    "/users/kennethdallmier/cathedral_engine/ash_archive_report.json",
    "/users/kennethdallmier/cathedral_engine/recommendations_ledger.md"
]
WEBHOOK_URL = "http://127.0.0.1:8000/api/terminal/webhook"

def send_terminal_alert(anomaly_message):
    payload = json.dumps({
        "source": "health_monitor",
        "severity": "CRITICAL",
        "message": anomaly_message
    }).encode("utf-8")
    
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            print(f"[Webhook] Alert successfully transmitted to terminal interface (Status: {response.getcode()})")
    except urllib.error.URLError as e:
        print(f"[Webhook] WARNING: Failed to reach terminal webhook endpoint: {e}", file=sys.stderr)

def check_system_health():
    anomalies_detected = False
    for ledger in LEDGERS:
        if not os.path.exists(ledger):
            msg = f"Critical ledger missing -> {ledger}"
            print(f"[Health Check] ERROR: {msg}", file=sys.stderr)
            send_terminal_alert(msg)
            anomalies_detected = True
            continue
        
        file_size = os.path.getsize(ledger)
        if ledger.endswith(".json"):
            try:
                with open(ledger, 'r') as f:
                    json.load(f)
                print(f"[Health Check] OK: {os.path.basename(ledger)} ({file_size} bytes) verified.")
            except json.JSONDecodeError as e:
                msg = f"Corrupted JSON structure in {ledger}: {e}"
                print(f"[Health Check] ERROR: {msg}", file=sys.stderr)
                send_terminal_alert(msg)
                anomalies_detected = True

    if not anomalies_detected:
        print("[Health Check] All operational strata and ledgers verified intact.")

if __name__ == "__main__":
    check_system_health()
