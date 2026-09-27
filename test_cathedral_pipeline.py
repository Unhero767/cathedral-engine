import sqlite3
import asyncio
import websockets
import json
import pathlib

DB_PATH = "ash_archive_stratum.db"
WS_URI = "ws://localhost:8765/ws/manifold"

def verify_sqlite_wal():
    print(f"[PIPELINE-TEST] Inspecting SQLite WAL database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM sqlite_master;")
    tables = cursor.fetchone()[0]
    conn.close()
    print(f"[SQLITE WAL] Journal Mode: {mode.upper()} | Active Tables/Strata: {tables}")
    assert mode.lower() == "wal", "Error: SQLite WAL mode is not active."

async def verify_websocket_manifold():
    print(f"[PIPELINE-TEST] Connecting to WebSocket telemetry manifold at {WS_URI}...")
    async with websockets.connect(WS_URI) as websocket:
        payload = {
            "event": "pipeline_integration_probe",
            "metrics": {
                "u_strain_glow_gain": 1.618,
                "monad_stratum_id": 36
            }
        }
        await websocket.send(json.dumps(payload))
        response = await websocket.recv()
        print(f"[MANIFOLD ACK] Received response: {response}")

if __name__ == "__main__":
    verify_sqlite_wal()
    asyncio.run(verify_websocket_manifold())
    print("[PIPELINE-TEST] Cathedral pipeline integration verification completed successfully.")
