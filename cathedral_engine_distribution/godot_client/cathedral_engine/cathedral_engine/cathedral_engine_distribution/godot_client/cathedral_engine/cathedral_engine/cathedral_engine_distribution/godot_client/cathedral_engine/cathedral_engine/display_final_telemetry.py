import urllib.request
import json
import sqlite3
import os

HTTP_URL = "http://localhost:5050/api/rpg/state"
DB_PATH = os.path.join("strata", "ash_archive.db")

print("================================================================================")
print(" 1. LIVE HTTP RPG STATE (/api/rpg/state)")
print("================================================================================")
try:
    req = urllib.request.Request(HTTP_URL, headers={"User-Agent": "CathedralCLI/1.0"})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"[-] HTTP Daemon notice: {e}")

print("\n================================================================================")
print(" 2. ASH ARCHIVE PERSISTENT STRATA (strata/ash_archive.db)")
print("================================================================================")
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
    p = c.fetchone()
    if p:
        print(f"• Player ID:         {p['player_id']}")
        print(f"• Active Chamber:    Chamber {p['current_chamber_id']} (Sanctum Apex / Core Monad)")
        print(f"• Position Vector:   ({p['coord_x']}, {p['coord_y']})")
        print(f"• Spectrum:          {p['active_spectrum']}")
        print(f"• Synchronized At:   {p['last_updated']}")

    c.execute("SELECT id, timestamp, content_hash, truth_value, dialetheic_flag, merkle_root FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    b = c.fetchone()
    if b:
        print(f"\n• Sealed Block ID:   #{b['id']}")
        print(f"• Content Hash:      {b['content_hash']}")
        print(f"• Merkle Root:       {b['merkle_root']}")
        print(f"• Belnap-Dunn Truth: {b['truth_value']} (Dialetheic Flag: {b['dialetheic_flag']})")
    
    conn.close()
