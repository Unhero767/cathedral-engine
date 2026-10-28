import sqlite3
import hashlib
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Cathedral-Engine: Ash Archive Merkle DAG")

def init_db():
    conn = sqlite3.connect('ash_archive.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temporal_strata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            state_payload TEXT NOT NULL,
            current_hash TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

class StateTransition(BaseModel):
    entity_id: str
    state_payload: dict

def generate_hash(previous_hash: str, payload: str) -> str:
    hasher = hashlib.sha256()
    hasher.update(previous_hash.encode('utf-8'))
    hasher.update(payload.encode('utf-8'))
    return hasher.hexdigest()

@app.post("/archive/transition")
def append_stratum(transition: StateTransition):
    conn = sqlite3.connect('ash_archive.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT current_hash FROM temporal_strata WHERE entity_id = ? ORDER BY id DESC LIMIT 1", 
        (transition.entity_id,)
    )
    result = cursor.fetchone()
    previous_hash = result[0] if result else "GENESIS_NULL"
    
    payload_str = json.dumps(transition.state_payload, sort_keys=True)
    current_hash = generate_hash(previous_hash, payload_str)
    
    cursor.execute(
        "INSERT INTO temporal_strata (entity_id, previous_hash, state_payload, current_hash) VALUES (?, ?, ?, ?)",
        (transition.entity_id, previous_hash, payload_str, current_hash)
    )
    conn.commit()
    conn.close()
    
    return {"status": "Stratum Appended", "hash": current_hash, "dialetheic_weight": len(payload_str)}

@app.get("/archive/history/{entity_id}")
def query_temporal_grammar(entity_id: str):
    conn = sqlite3.connect('ash_archive.db')
    cursor = conn.cursor()
    cursor.execute("SELECT previous_hash, current_hash, state_payload, timestamp FROM temporal_strata WHERE entity_id = ? ORDER BY id ASC", (entity_id,))
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    chronological_mass = 0
    for r in rows:
        payload_size = len(r[2])
        chronological_mass += payload_size
        history.append({
            "previous_hash": r[0],
            "current_hash": r[1],
            "payload_size_bytes": payload_size,
            "timestamp": r[3]
        })
        
    return {
        "entity_id": entity_id, 
        "strata_count": len(history), 
        "chronological_mass_bytes": chronological_mass, 
        "temporal_strata": history
    }

init_db()
