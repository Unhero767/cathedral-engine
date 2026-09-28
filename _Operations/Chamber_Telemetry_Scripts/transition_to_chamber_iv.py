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
    req = urllib.request.Request(url, headers={"User-Agent": "CathedralNavigator/1.0"})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

print("==================================================")
print(" 1. CROSSING GATEWAY THRESHOLD -> CHAMBER IV")
print("==================================================")

# Step into Chamber IV entry coords (0, 4)
move_params = {"x": 0, "y": 4, "chamber": 4}
try:
    print("[*] Initiating gateway handshake...")
    res = get("move", move_params)
    print("Move Response:", json.dumps(res, indent=2))
except Exception as e:
    print("[-] HTTP Move request notice:", e)

# Trigger Chamber transition hook
try:
    print("[*] Retrieving Chamber IV manifest (/api/rpg/chamber?id=4)...")
    ch_res = get("chamber", {"id": 4})
    print(f"Chamber Designation: {ch_res.get('name', 'Chamber IV: Unknown Resonant Strata')}")
    print(f"Carrier Frequency:   {ch_res.get('carrier_hz', 78.2)} Hz")
except Exception as e:
    print("[-] Chamber query notice:", e)

print("\n==================================================")
print(" 2. COMMITTING VAULT TRANSITION TO ASH ARCHIVE")
print("==================================================")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    timestamp_iso = datetime.now(timezone.utc).isoformat()
    
    # Fetch latest hash for chain integrity
    c.execute("SELECT content_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    parent_hash = row[0] if row else "0" * 64
    
    payload = {
        "event": "CHAMBER_TRANSITION",
        "origin_chamber": 3,
        "destination_chamber": 4,
        "entry_coordinates": {"x": 0, "y": 4},
        "spectral_shift": {
            "previous": "Blue / Pneumatic Sorrow (65.4 Hz)",
            "active": "Resonant Strata (78.2 Hz)"
        }
    }
    
    payload_str = json.dumps(payload, sort_keys=True)
    content_hash = hashlib.sha256(f"{parent_hash}:{payload_str}:{timestamp_iso}".encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(f"{content_hash}:{timestamp_iso}".encode("utf-8")).hexdigest()
    scar_hash = hashlib.sha256(f"SCAR:VAULT_TRANSITION:{content_hash}".encode("utf-8")).hexdigest()
    
    try:
        # Append immutable block
        c.execute("""
            INSERT INTO ash_ledger (
                timestamp, parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (timestamp_iso, parent_hash, content_hash, payload_str, 0, "TRUE", merkle_root))
        
        # Update player_state record
        c.execute("""
            UPDATE player_state
            SET current_chamber_id = 4,
                coord_x = 0,
                coord_y = 4,
                active_spectrum = 'Resonant',
                last_updated = CURRENT_TIMESTAMP
            WHERE player_id = 'player_primary';
        """)
        conn.commit()
        print(f"[+] Transition finalized. Block: {content_hash[:20]}...")
    except Exception as err:
        print("[-] Database update error:", err)
    finally:
        conn.close()

print("\n==================================================")
print(" 3. ACTIVE SUBSTRATE TELEMETRY")
print("==================================================")
print("• Status:            Chamber IV Entry Initialized")
print("• Coordinate:        (0, 4)")
print("• Spectral Domain:   Resonant / Higher Harmonic")
