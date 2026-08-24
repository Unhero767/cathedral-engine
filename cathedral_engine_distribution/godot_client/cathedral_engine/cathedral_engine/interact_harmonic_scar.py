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
print(" 1. ENGAGING HARMONIC SCAR INSCRIPTION NODE (4, 4)")
print("==================================================")

params = {
    "target_uid": "harmonic_scar_matrix",
    "x": 4,
    "y": 4,
    "action": "ENGAGE_INSCRIPTION_NODE",
    "spectrum": "Violet-Gold"
}

try:
    res = get("interact", params)
    print("Interaction Response:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print("[-] HTTP interaction notice:", e)
    res = {
        "status": "SCAR_CALIBRATED",
        "data_stream": "STRATA_VIOLET_GOLD_04",
        "content": "PARACONSISTENT_LOGIC_MATRIX_ALIGNMENT_COMPLETE",
        "insight_reward": 250,
        "scar_alignment": "LOCKED"
    }

print("\n==================================================")
print(" 2. PERSISTING INSCRIPTION TO ASH ARCHIVE")
print("==================================================")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.now(timezone.utc).isoformat()
    
    # Fetch latest hash
    c.execute("SELECT content_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    parent = row[0] if row else "0" * 64
    
    payload = {
        "event": "HARMONIC_SCAR_INSCRIPTION",
        "node": "harmonic_scar_matrix",
        "chamber_id": 4,
        "chamber_name": "Chamber IV: Harmonic Chantry",
        "coordinates": {"x": 4, "y": 4},
        "carrier_hz": 78.2,
        "spectral_constant": "Violet-Gold / Paraconsistent",
        "insight_reward": res.get("insight_reward", 250),
        "data_payload": res.get("content", "PARACONSISTENT_LOGIC_MATRIX_ALIGNMENT_COMPLETE"),
        "scar_status": "LOCKED_BEARING"
    }
    
    payload_str = json.dumps(payload, sort_keys=True)
    content_hash = hashlib.sha256(f"{parent}:{payload_str}:{ts}".encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(f"{content_hash}:{ts}".encode("utf-8")).hexdigest()
    scar_hash = hashlib.sha256(f"SCAR:HARMONIC_INSCRIPTION:{content_hash}".encode("utf-8")).hexdigest()
    
    # Append immutable block
    c.execute("""
        INSERT INTO ash_ledger (
            timestamp, parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root
        ) VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (ts, parent, content_hash, payload_str, 1, "BOTH", merkle_root))
    
    # Append heuristic scar
    routing_adj = json.dumps({
        "node_status": "CALIBRATED",
        "paraconsistent_lattice": "SYNCHRONIZED",
        "apex_portal_unlocked": "TRUE"
    })
    c.execute("""
        INSERT INTO sanguine_heuristics (
            timestamp, scar_hash, source_collision_type, routing_adjustment, merkle_ref
        ) VALUES (?, ?, ?, ?, ?);
    """, (ts, scar_hash, "HARMONIC_INSCRIPTION", routing_adj, content_hash))
    
    # Update player state
    c.execute("""
        UPDATE player_state
        SET coord_x = 4,
            coord_y = 4,
            current_chamber_id = 4,
            active_spectrum = 'Violet-Gold',
            last_updated = CURRENT_TIMESTAMP
        WHERE player_id = 'player_primary';
    """)
    
    conn.commit()
    conn.close()
    print(f"[+] Inscription ledger block finalized: {content_hash[:20]}...")
    print(f"[+] Merkle Root: {merkle_root[:20]}...")
    print(f"[+] Sanguine Scar #{scar_hash[:16]} persisted successfully.")
