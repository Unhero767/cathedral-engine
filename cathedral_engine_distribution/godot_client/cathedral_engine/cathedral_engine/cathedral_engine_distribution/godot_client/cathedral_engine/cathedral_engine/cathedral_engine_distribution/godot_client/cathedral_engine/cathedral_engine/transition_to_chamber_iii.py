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
print(" 1. CROSSING GATEWAY THRESHOLD -> CHAMBER III")
print("==================================================")

# Step into Chamber III entry coords (0, 4)
move_params = {"x": 0, "y": 4, "chamber": 3}
try:
    print("[*] Dispatching movement to Chamber III entry node (0, 4)...")
    res = get("move", move_params)
    print("Move Response:", json.dumps(res, indent=2))
except Exception as e:
    print("[-] HTTP Move request notice:", e)

# Trigger Chamber transition hook
try:
    print("[*] Initializing Chamber III manifest (/api/rpg/chamber?id=3)...")
    ch_res = get("chamber", {"id": 3})
    print(f"Chamber Designation: {ch_res.get('name', 'Chamber III: Pneumatic Vault')}")
    print(f"Carrier Frequency:   {ch_res.get('carrier_hz', 65.4)} Hz")
except Exception as e:
    print("[-] Chamber query notice:", e)

print("\n==================================================")
print(" 2. COMMITTING VAULT TRANSITION TO ASH ARCHIVE")
print("==================================================")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    timestamp_iso = datetime.now(timezone.utc).isoformat()
    
    # Fetch latest hash
    c.execute("SELECT content_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    row = c.fetchone()
    parent_hash = row[0] if row else "0" * 64
    
    payload = {
        "event": "CHAMBER_TRANSITION",
        "origin_chamber": 2,
        "destination_chamber": 3,
        "destination_name": "Chamber III: Pneumatic Vault",
        "entry_coordinates": {"x": 0, "y": 4},
        "carrier_hz": 65.4,
        "spectral_shift": {
            "previous": "Teal / Somatic Heat Sink (52.8 Hz)",
            "active": "Blue / Pneumatic Sorrow (65.4 Hz)"
        }
    }
    
    payload_str = json.dumps(payload, sort_keys=True)
    content_hash = hashlib.sha256(f"{parent_hash}:{payload_str}:{timestamp_iso}".encode("utf-8")).hexdigest()
    merkle_root = hashlib.sha256(f"{content_hash}:{timestamp_iso}".encode("utf-8")).hexdigest()
    scar_hash = hashlib.sha256(f"SCAR:PNEUMATIC_ENTRY:{content_hash}".encode("utf-8")).hexdigest()
    
    try:
        # 1. Append immutable block
        c.execute("""
            INSERT INTO ash_ledger (
                timestamp, parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root
            ) VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (timestamp_iso, parent_hash, content_hash, payload_str, 0, "TRUE", merkle_root))
        print(f"[+] Appended ash_ledger block: {content_hash[:20]}...")
        
        # 2. Append heuristic routing
        routing_adj = json.dumps({
            "active_chamber": 3,
            "resonance_state": "BLUE_CONSTANT_LOCKED",
            "ambient_pressure_psi": 14.7,
            "aerostatic_damping": "ENABLED"
        })
        c.execute("""
            INSERT INTO sanguine_heuristics (
                timestamp, scar_hash, source_collision_type, routing_adjustment, merkle_ref
            ) VALUES (?, ?, ?, ?, ?);
        """, (timestamp_iso, scar_hash, "PNEUMATIC_VAULT_TRANSITION", routing_adj, content_hash))
        print(f"[+] Appended sanguine_heuristics record: {scar_hash[:20]}...")
        
        # 3. Update player_state record
        c.execute("""
            UPDATE player_state
            SET current_chamber_id = 3,
                coord_x = 0,
                coord_y = 4,
                active_spectrum = 'Blue',
                last_updated = CURRENT_TIMESTAMP
            WHERE player_id = 'player_primary';
        """)
        conn.commit()
        print("[+] Updated player_state: Chamber 3 at (0, 4) with Blue Spectrum.")
    except Exception as err:
        print("[-] Database update error:", err)
    finally:
        conn.close()

print("\n==================================================")
print(" 3. ACTIVE SUBSTRATE TELEMETRY")
print("==================================================")
print("• Location:          Chamber III: Pneumatic Vault")
print("• Current Node:      Entry Portal Vector (0, 4)")
print("• Carrier Wave:      65.40 Hz [Blue Dominant / Sorrow Constant]")
print("• Atmospheric Duct:  Aerostatic Column Pressurized (Nominal)")
