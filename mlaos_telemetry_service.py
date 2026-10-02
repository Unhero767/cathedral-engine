import asyncio
import json
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Cathedral-Engine Ash Archive Telemetry Gateway", version="Ω-ONT-001")

# Enable CORS for local Three.js visualizer (Port 8080 -> Port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "ash_archive.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_stream (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            tier TEXT,
            payload TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class TelemetryEvent(BaseModel):
    tier: str
    payload: dict

@app.get("/")
def read_root():
    return {"status": "Ash Archive Telemetry Gateway Operational", "version": "Ω-ONT-001"}

@app.post("/telemetry")
def post_telemetry(event: TelemetryEvent):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telemetry_stream (tier, payload) VALUES (?, ?)",
        (event.tier, json.dumps(event.payload))
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"status": "recorded", "id": new_id}

@app.get("/stream")
async def stream_telemetry():
    async def event_generator():
        last_id = 0
        yield f"data: {json.dumps({'message': 'Connected to Ash Archive SSE Stream'})}\n\n"
        while True:
            try:
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id, timestamp, tier, payload FROM telemetry_stream WHERE id > ? ORDER BY id ASC", (last_id,))
                rows = cursor.fetchall()
                conn.close()
                
                for row in rows:
                    last_id = row["id"]
                    try:
                        parsed_payload = json.loads(row["payload"])
                    except Exception:
                        parsed_payload = {"raw": row["payload"]}
                        
                    data = {
                        "id": row["id"],
                        "timestamp": row["timestamp"],
                        "tier": row["tier"],
                        "payload": parsed_payload
                    }
                    yield f"data: {json.dumps(data)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            await asyncio.sleep(1.0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
