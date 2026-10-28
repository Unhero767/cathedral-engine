from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import sqlite3
import asyncio
import json

app = FastAPI(title="Cathedral-Engine Telemetry Manifold", version="4.8.2")
DB_PATH = "ash_archive_stratum.db"

@app.get("/api/v1/manifold/status")
async def get_manifold_status():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ash_nodes;")
    count = cursor.fetchone()[0]
    conn.close()
    return {"status": "ACTIVE", "lex_invariant": "LEX_I_SECURE", "strata_count": count}

@app.websocket("/ws/manifold")
async def websocket_manifold_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT record_id, proposition_id, evidence_positive, evidence_negative, resolution_status FROM ash_nodes ORDER BY timestamp DESC LIMIT 5;")
            rows = cursor.fetchall()
            conn.close()
            
            telemetry_payload = {
                "engine": "MLAOS-Prime // Cathedral-Engine",
                "spectral_constant": "EMERALD/LOVE",
                "strain_threshold": 2.56,
                "strata": [{"record_id": r[0], "prop": r[1], "pos": r[2], "neg": r[3], "status": r[4]} for r in rows]
            }
            await websocket.send_text(json.dumps(telemetry_payload))
            await asyncio.sleep(2.0)
    except WebSocketDisconnect:
        print("[*] Manifold WebSocket client disconnected.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8765)

# --- BOOK XXII CANONICAL VERIFICATION DOSSIER ROUTER ---
from routers.cathedral_dossier import router as cathedral_dossier_router
app.include_router(cathedral_dossier_router)
