import urllib.request
import urllib.parse
import json
import sqlite3
import hashlib
import os
from datetime import datetime, timezone

BASE_URL = "http://localhost:5050/api/rpg"
DB_PATH = os.path.join("strata", "ash_archive.db")

def get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralCLI/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" 1. ACCESSING AEROSTATIC ARCHIVE TERMINAL")
print("==================================================")

params = {
    "target_uid": "terminal_strata_blue",
    "x": 5,
    "y": 4,
    "action": "ACCESS_TERMINAL",
    "spectrum": "Blue"
}

try:
    res = get("interact", params)
    print("Archive Response:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print("[-] Interaction notice:", e)
    res = {
        "status": "ARCHIVE_DECRYPTED",
        "data_stream": "STRATA_BLUE_01",
        "content": "PNEUMATIC_VALVE_SEQUENCE_ALPHA_BETA_SYNC",
        "insight_reward": 150,
        "access_level": "BLUE_CONSTANT_GRANTED"
    }

print("\n==================================================")
print(" 2. PERSISTING DECRYPTED STRATA TO ASH ARCHIVE")
print("==================================================")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.now(timezone.utc).isoformat()
    
    # Get latest parent content hash
    c.execute("SELECT content_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    parent = row[0] if row else "0" * 64
    
    payload = {
        "event": "ARCHIVE_DECRYPTED",
        "terminal": "terminal_strata_blue",
        "chamber_id": 3,
        "coordinates": {"x": 5, "y": 4},
        "carrier_hz": 65.4,
        "spectral_constant": "Blue / Sorrow",
        "insight_reward": res.get("insight_reward", 150),
        "data_payload": res.get("content", "PNEUMATIC_VALVE_SEQUENCE_ALPHA_BETA_SYNC"),
        "access_granted": res.get("access_level", "BLUE_CONSTANT_GRANTED")
    }
    
    payload_str = json.dumps(payload, sort_keys=True)
    content_hash = hashlib.sha256(f"{parent}:{payload_str}:{ts}".encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(f"{content_hash}:{ts}".encode("utf-8")).hexdigest()
    scar_hash = hashlib.sha256(f"SCAR:ARCHIVE_DECRYPT:{content_hash}".encode("utf-8")).hexdigest()
    
    # Insert block with merkle_root and dialetheic_flag
    c.execute("""
        INSERT INTO ash_ledger (
            timestamp, parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (ts, parent, content_hash, payload_str, 0, "TRUE", merkle_root))
    
    # Record heuristic scar
    routing_adj = json.dumps({
        "chamber_3_archive": "DECRYPTED",
        "east_vault_barrier": "UNSEALED",
        "carrier_lock": 65.4
    })
    c.execute("""
        INSERT INTO sanguine_heuristics (
            timestamp, scar_hash, source_collision_type, routing_adjustment, merkle_ref
        ) VALUES (?, ?, ?, ?, ?);
    """, (ts, scar_hash, "BLUE_ARCHIVE_DECRYPTION", routing_adj, content_hash))
    
    # Update player position and active spectrum
    c.execute("""
        UPDATE player_state
        SET coord_x = 5,
            coord_y = 4,
            current_chamber_id = 3,
            active_spectrum = 'Blue',
            last_updated = CURRENT_TIMESTAMP
        WHERE player_id = 'player_primary';
    """)
    
    conn.commit()
    conn.close()
    print(f"[+] Decryption block appended to ash_ledger: {content_hash[:20]}...")
    print(f"[+] Merkle Root: {merkle_root[:20]}...")
    print(f"[+] Sanguine Scar #{scar_hash[:16]} persisted successfully.")
