import sqlite3
import os
import urllib.request
import json

def test_database():
    print("[TEST 1/4] Verifying Ash Archive SQLite WAL database...")
    assert os.path.exists("ash_archive.db"), "ash_archive.db missing!"
    conn = sqlite3.connect("ash_archive.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    assert mode.lower() == "wal", f"Expected WAL mode, got {mode}"
    cursor.execute("SELECT COUNT(*) FROM ash_ledger;")
    count = cursor.fetchone()[0]
    conn.close()
    print(f" -> PASSED: Database active in WAL mode with {count} ledger entries.")

def test_reconciliation():
    print("[TEST 2/4] Testing Magisterial Arbiter reconciliation node insertion...")
    import mlaos_arbiter_reconciliation
    mlaos_arbiter_reconciliation.reconcile_fracture_nodes()
    conn = sqlite3.connect("ash_archive.db")
    cursor = conn.cursor()
    cursor.execute("SELECT current_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    h = cursor.fetchone()[0]
    conn.close()
    assert h is not None and len(h) == 64, "Invalid hash lineage generated."
    print(f" -> PASSED: Synthesis block committed with hash lineage: {h[:16]}...")

def test_comfy_connection():
    print("[TEST 3/4] Checking ComfyUI local API connectivity (port 8188)...")
    try:
        req = urllib.request.Request("http://127.0.0.1:8188/system_stats")
        with urllib.request.urlopen(req, timeout=2) as response:
            print(" -> PASSED: ComfyUI server is online and reachable.")
    except Exception as e:
        print(f" -> NOTICE: ComfyUI server is offline or unreachable ({e}). (Safe to ignore if ComfyUI isn't currently booted)")

def test_telemetry_snapshot():
    print("[TEST 4/4] Testing Telemetry snapshot logic...")
    import mlaos_telemetry_service
    snapshot = mlaos_telemetry_service.telemetry_snapshot()
    assert snapshot["status"] == "active", "Telemetry snapshot inactive!"
    print(f" -> PASSED: Telemetry snapshot active, retrieved {len(snapshot['recent_nodes'])} recent nodes.")

if __name__ == "__main__":
    print("==========================================================")
    print("        CATHEDRAL-ENGINE PIPELINE INTEGRATION TEST        ")
    print("==========================================================")
    test_database()
    test_reconciliation()
    test_comfy_connection()
    test_telemetry_snapshot()
    print("==========================================================")
    print("       ALL CORE PIPELINE VERIFICATIONS COMPLETED          ")
    print("==========================================================")
