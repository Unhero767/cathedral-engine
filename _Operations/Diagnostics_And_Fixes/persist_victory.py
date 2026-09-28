import sqlite3
import hashlib
import json
import os
from datetime import datetime, timezone

DB_PATH = os.path.join("strata", "ash_archive.db")

print("==================================================")
print(" PERSISTING COMBAT VICTORY & TRI-KEY REWARD")
print("==================================================")

if not os.path.exists(DB_PATH):
    print(f"[-] Database not found at: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")

# --- 1. Compute Cryptographic Strata Hashes ---
timestamp_iso = datetime.now(timezone.utc).isoformat()

# Fetch latest parent content hash from ash_ledger
c.execute("SELECT content_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
row = c.fetchone()
parent_hash = row[0] if row else "0" * 64

victory_payload = {
    "event": "COMBAT_VICTORY",
    "target_uid": "enemy_sentinel_01",
    "target_name": "Lithic Sentinel",
    "spectrum_resolved": "Bronze-Obsidian",
    "turns_elapsed": 3,
    "rewards": {
        "relic": "OBJ_TRIKEY_LEAD",
        "insight": 50,
        "quest_resolved": "Q_LITHIC_GENESIS"
    },
    "chamber_anchor": "Chamber I: Lithic Foundation (43.7 Hz)"
}

payload_str = json.dumps(victory_payload, sort_keys=True)
content_hash = hashlib.sha256(f"{parent_hash}:{payload_str}:{timestamp_iso}".encode("utf-8")).hexdigest()
merkle_root = hashlib.sha256(f"{content_hash}:{timestamp_iso}".encode("utf-8")).hexdigest()
scar_hash = hashlib.sha256(f"SCAR:LITHIC_RESOLVE:{content_hash}".encode("utf-8")).hexdigest()

# --- 2. Append to Immutable ash_ledger ---
try:
    c.execute("""
        INSERT INTO ash_ledger (
            timestamp, parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (timestamp_iso, parent_hash, content_hash, payload_str, 0, "TRUE", merkle_root))
    print(f"[+] Appended ash_ledger block: {content_hash[:16]}...")
except sqlite3.OperationalError as e:
    print(f"[-] ash_ledger write notice: {e}")

# --- 3. Append to Sanguine Heuristics Ledger ---
try:
    routing_adjustment = json.dumps({
        "chamber_unlocked": 2,
        "attenuation_hz": 43.7,
        "resonance_gate": "GATE_SOMATIC_OPEN"
    })
    c.execute("""
        INSERT INTO sanguine_heuristics (
            timestamp, scar_hash, source_collision_type, routing_adjustment, merkle_ref
        ) VALUES (?, ?, ?, ?, ?);
    """, (timestamp_iso, scar_hash, "LITHIC_SENTINEL_SHATTER", routing_adjustment, content_hash))
    print(f"[+] Appended sanguine_heuristics record: {scar_hash[:16]}...")
except sqlite3.OperationalError as e:
    print(f"[-] sanguine_heuristics write notice: {e}")

# --- 4. Update player_state Inventory & Progression ---
c.execute("SELECT inventory_json FROM player_state WHERE player_id = 'player_primary';")
player_row = c.fetchone()

if player_row:
    try:
        inv = json.loads(player_row[0]) if player_row[0] else {}
    except Exception:
        inv = {}
        
    inv["OBJ_TRIKEY_LEAD"] = {
        "name": "Basalt Tri-Key of Lead",
        "type": "CHAMBER_KEY",
        "description": "Grounds the 43.7 Hz carrier wave. Unlocks Chamber II Somatic Gateway.",
        "quantity": 1,
        "spectral_constant": "Gold/Lead"
    }
    
    c.execute("""
        UPDATE player_state
        SET inventory_json = ?,
            current_chamber_id = 2,
            last_updated = CURRENT_TIMESTAMP
        WHERE player_id = 'player_primary';
    """, (json.dumps(inv),))
    print("[+] Updated player_state: Added OBJ_TRIKEY_LEAD and advanced chamber to 2.")
else:
    init_inv = json.dumps({
        "OBJ_TRIKEY_LEAD": {
            "name": "Basalt Tri-Key of Lead",
            "type": "CHAMBER_KEY",
            "description": "Grounds the 43.7 Hz carrier wave. Unlocks Chamber II Somatic Gateway.",
            "quantity": 1,
            "spectral_constant": "Gold/Lead"
        }
    })
    c.execute("""
        INSERT INTO player_state (
            player_id, current_chamber_id, coord_x, coord_y, active_spectrum, health, max_health, inventory_json
        ) VALUES ('player_primary', 2, 4, 4, 'Gold', 20, 20, ?);
    """, (init_inv,))
    print("[+] Created player_primary state record with OBJ_TRIKEY_LEAD.")

conn.commit()
conn.close()

print("[+] Transaction complete. State locked in immutable ledger.")
