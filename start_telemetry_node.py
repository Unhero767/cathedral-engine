#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import sqlite3
from pathlib import Path
import asyncio
import json
from datetime import datetime, timezone

app = FastAPI(title="Cathedral-Engine Ash Archive Telemetry Node")
DB_PATH = "ash_archive_stratum.db"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "cathedral-telemetry-node"}

@app.get("/api/v1/ash/merkle/root")
def get_merkle_root():
    if not Path(DB_PATH).exists():
        return {"error": "Ash archive database not initialized."}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT merkle_hash, timestamp FROM ash_archive_stratum ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"merkle_root": None}
    return {"merkle_root": row[0], "timestamp": row[1]}

@app.get("/api/v1/ash/query/temporal")
def query_temporal():
    if not Path(DB_PATH).exists():
        return {"error": "Ash archive database not initialized."}
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, payload, parent_hash, merkle_hash, timestamp FROM ash_archive_stratum ORDER BY id ASC;")
    rows = cursor.fetchall()
    conn.close()
    
    blocks = []
    for r in rows:
        blocks.append({
            "id": r[0],
            "payload": r[1],
            "parent_hash": r[2],
            "merkle_hash": r[3],
            "timestamp": r[4]
        })
    return {"blocks": blocks}

@app.websocket("/ws/manifold")
async def websocket_manifold(websocket: WebSocket):
    await websocket.accept()
    print("==> [WebSocket] Client connected to /ws/manifold telemetry manifold.")
    try:
        step = 0
        while True:
            step += 1
            # Simulate real-time dPhi/dt telemetry stream coupled with Belnap-Dunn states
            payload = {
                "step": step,
                "dPhi_dt": 0.42 * (1.0 + 0.1 * (step % 10)),
                "belnap_state": "Both",
                "harmonic_scar_active": True,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(0.1) # 10 Hz telemetry tick
    except WebSocketDisconnect:
        print("==> [WebSocket] Client disconnected from /ws/manifold.")

if __name__ == "__main__":
    print("==> Starting Uvicorn Telemetry Node with /ws/manifold on http://127.0.0.1:8765 ...")
    uvicorn.run(app, host="127.0.0.1", port=8765)

import httpx
from pydantic import BaseModel

class AvatarGenerationRequest(BaseModel):
    seed_prompt: str = "Cathedral sovereign mechanoid saint, gothic biomechanical chassis"
    dphi_dt: float = 0.42
    belnap_state: str = "Both"

@app.post("/api/v1/avatar/generate")
async def generate_avatar_webhook(payload: AvatarGenerationRequest):
    comfy_url = "http://127.0.0.1:8188/prompt"
    
    # Construct prompt incorporating MLAOS-HGASE art direction & spectral telemetry
    enhanced_prompt = (
        f"{payload.seed_prompt}, hard-noir biomechanical gothic 32-bit HD-2D, volumetric chiaroscuro lighting, "
        f"spectral frequency gold joy, dPhi_dt={payload.dphi_dt:.2f}, belnap_state={payload.belnap_state}"
    )
    
    workflow_payload = {
        "prompt": {
            "3": {
                "inputs": {
                    "text": enhanced_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            }
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(comfy_url, json=workflow_payload)
            if response.status_code == 200:
                return {"status": "success", "comfy_response": response.json()}
            else:
                return {"status": "proxied_local_fallback", "prompt": enhanced_prompt, "note": "ComfyUI offline; payload formatted."}
    except Exception as e:
        return {"status": "simulated_dispatch", "prompt": enhanced_prompt, "error": str(e)}
