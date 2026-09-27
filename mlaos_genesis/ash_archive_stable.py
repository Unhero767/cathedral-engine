import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Ash Archive - Character Stable Engine",
    description="Thermodynamic asset management and cryogenic vault telemetry for the Cathedral-Engine.",
    version="2.0.0"
)

DB_PATH = "ash_archive.db"

class AssetMutationRequest(BaseModel):
    entity_name: str
    target_guild: str
    new_level: int

class AssetRegistrationModel(BaseModel):
    asset_id: str
    entity_name: str
    race: str
    alignment: str
    guild: str
    level: int
    status: Optional[str] = "VAULTED"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Character Stable Master Schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS character_stable (
            asset_id TEXT PRIMARY KEY,
            entity_name TEXT NOT NULL UNIQUE,
            status TEXT CHECK(status IN ('ACTIVE', 'VAULTED')) NOT NULL,
            race TEXT NOT NULL,
            alignment TEXT NOT NULL,
            guild TEXT NOT NULL,
            level INTEGER NOT NULL,
            chronological_mass REAL DEFAULT 1000.0,
            policy_violations INTEGER DEFAULT 0,
            multiclass_penalties REAL DEFAULT 0.0
        )
    """)
    
    # Seed initial assets if registry is pristine
    cursor.execute("SELECT COUNT(*) FROM character_stable")
    if cursor.fetchone()[0] == 0:
        seed_assets = [
            ("ASSET_01", "Janus_Stoneblood", "ACTIVE", "Osiri", "Lawful Neutral", "Sorcerer", 20, 1524.0, 0, 0.0),
            ("ASSET_02", "Kaelen_Vex", "ACTIVE", "Morloch", "Chaotic Neutral", "Warrior", 18, 43100.0, 2, 0.0),
            ("ASSET_03", "Vesper_Null", "VAULTED", "Osiri", "True Neutral", "Acolyte", 5, 200.0, 0, 0.0),
            ("ASSET_04", "Lyra_Silent", "VAULTED", "Morloch", "Lawful Evil", "Architect", 1, 100.0, 0, 0.0)
        ]
        cursor.executemany("INSERT INTO character_stable VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", seed_assets)
        conn.commit()
    
    conn.close()

init_db()

@app.get("/archive/stable/status")
async def get_stable_status():
    """Returns the complete telemetry of active deployments and vaulted reserves."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM character_stable")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    active_assets = [r for r in rows if r["status"] == "ACTIVE"]
    vaulted_assets = [r for r in rows if r["status"] == "VAULTED"]
    
    return {
        "active_deployment_count": len(active_assets),
        "vaulted_reserve_count": len(vaulted_assets),
        "roster": rows
    }

@app.post("/archive/stable/deploy/{entity_name}")
async def deploy_asset(entity_name: str):
    """Shifts an asset from the cryogenic vault to active deployment (Max 4 ceiling)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM character_stable WHERE entity_name = ?", (entity_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Asset not found in Stable registry.")
        
    if row[0] == "ACTIVE":
        conn.close()
        raise HTTPException(status_code=400, detail="Asset is already deployed.")
        
    cursor.execute("SELECT COUNT(*) FROM character_stable WHERE status = 'ACTIVE'")
    active_count = cursor.fetchone()[0]
    
    if active_count >= 4:
        conn.close()
        raise HTTPException(status_code=403, detail="Active deployment ceiling reached (Max 4). Vault release denied.")
        
    cursor.execute("UPDATE character_stable SET status = 'ACTIVE' WHERE entity_name = ?", (entity_name,))
    conn.commit()
    conn.close()
    
    return {"status": "SUCCESS", "message": f"Asset {entity_name} successfully extracted from cryogenic vault to active deployment."}

@app.post("/archive/stable/vault/{entity_name}")
async def vault_asset(entity_name: str):
    """Returns an active asset to the null-state cryogenic reserve."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM character_stable WHERE entity_name = ?", (entity_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Asset not found in Stable registry.")
        
    if row[0] == "VAULTED":
        conn.close()
        raise HTTPException(status_code=400, detail="Asset is already in cryogenic stasis.")
        
    cursor.execute("UPDATE character_stable SET status = 'VAULTED' WHERE entity_name = ?", (entity_name,))
    conn.commit()
    conn.close()
    
    return {"status": "SUCCESS", "message": f"Asset {entity_name} returned to cryogenic sanctuary."}

@app.get("/archive/history/{entity_id}")
async def get_entity_history(entity_id: str):
    """Retrieves chronological mass, historical friction, and multiclass penalties for a specific asset."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM character_stable WHERE entity_name = ?", (entity_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Asset not found in Character Stable.")
        
    data = dict(row)
    return {
        "entity_id": data["entity_name"],
        "status": data["status"],
        "race": data["race"],
        "guild": data["guild"],
        "level": data["level"],
        "chronological_mass_bytes": data["chronological_mass"],
        "policy_violations": data["policy_violations"],
        "multiclass_penalty": data["multiclass_penalties"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
