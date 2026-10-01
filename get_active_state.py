import urllib.request
import json
import sqlite3
import os

BASE_URL = "http://localhost:5050/api/rpg/state"
DB_PATH = os.path.join("strata", "ash_archive.db")

print("================================================================================")
print(" 1. HTTP RPG STATE (/api/rpg/state)")
print("================================================================================")
try:
    req = urllib.request.Request(BASE_URL, headers={"User-Agent": "CathedralCLI/1.0"})
    with urllib.request.urlopen(req) as res:
        state_data = json.loads(res.read().decode())
        print(json.dumps(state_data, indent=2))
except Exception as e:
    print(f"[-] HTTP Query notice: {e}")

print("\n================================================================================")
print(" 2. SQLITE ASH ARCHIVE CURRENT STRATA")
print("================================================================================")
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
    p = c.fetchone()
    if p:
        print(f"• Player ID:         {p['player_id']}")
        print(f"• Chamber ID:        Chamber {p['current_chamber_id']}")
        print(f"• Coordinate Vector: ({p['coord_x']}, {p['coord_y']})")
        print(f"• Active Spectrum:   {p['active_spectrum']}")
        print(f"• Last Synchronized: {p['last_updated']}")
        
    c.execute("SELECT id, timestamp, content_hash, truth_value, dialetheic_flag, merkle_root FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    b = c.fetchone()
    if b:
        print(f"\n• Latest Block ID:   #{b['id']}")
        print(f"• Content Hash:      {b['content_hash']}")
        print(f"• Merkle Root:       {b['merkle_root']}")
        print(f"• Truth Value:       {b['truth_value']} (Dialetheic Flag: {b['dialetheic_flag']})")
    conn.close()
