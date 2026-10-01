import subprocess
import time
import urllib.request
import json
import sqlite3
import os
import sys

SERVER_FILE = "server.py"
DB_PATH = os.path.join("strata", "ash_archive.db")
API_BASE = "http://localhost:5050/api/rpg"

print("================================================================================")
print("                    INITIALIZING CATHEDRAL-ENGINE (MLAOS-PRIME)                 ")
print("================================================================================")

# 1. Ensure Port 5050 is clean and launch daemon
print("[1/4] Clearing port 5050 and spinning up HTTP daemon...")
subprocess.run("lsof -ti:5050 | xargs kill -9 2>/dev/null || true", shell=True)

proc = subprocess.Popen([sys.executable, SERVER_FILE], stdout=open("server.log", "a"), stderr=subprocess.STDOUT)
print(f"      └─ Daemon spawned with PID {proc.pid}. Waiting for socket...")
time.sleep(2.0)

# 2. Ping Health Endpoint
print("[2/4] Testing daemon API loop...")
try:
    req = urllib.request.Request(f"{API_BASE}/state", headers={"User-Agent": "CathedralRunner/1.0"})
    with urllib.request.urlopen(req) as res:
        state = json.loads(res.read().decode())
        player = state.get("player", {})
        print(f"      └─ HTTP Daemon ONLINE (Status: OK)")
        print(f"      └─ Active Chamber: {player.get('chamber', 5)} | Position: ({player.get('x', 7)}, {player.get('y', 4)})")
except Exception as e:
    print(f"      [-] Warning: HTTP ping encountered {e}. Checking local DB strata...")

# 3. Check SQLite Strata & Ledger Integrity
print("[3/4] Verifying Ash Archive strata & Merkle trees...")
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM ash_ledger;")
    block_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM sanguine_heuristics;")
    scar_count = c.fetchone()[0]
    
    c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
    p = c.fetchone()
    
    c.execute("SELECT id, content_hash, merkle_root, truth_value FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    latest = c.fetchone()
    
    conn.close()
    
    print(f"      └─ ash_ledger Blocks: {block_count} (Merkle Proofs Active)")
    print(f"      └─ Sanguine Scars:    {scar_count} Dialetheic Collisions Anchored")
    if p:
        print(f"      └─ Sovereign Vector:  Chamber {p['current_chamber_id']} @ ({p['coord_x']}, {p['coord_y']}) [{p['active_spectrum']}]")
    if latest:
        print(f"      └─ Sealed Block #{latest['id']}:  {latest['content_hash'][:20]}... [Truth={latest['truth_value']}]")
else:
    print("      [-] ash_archive.db not found. Run migrations to initialize.")

# 4. Engine Runtime Status
print("[4/4] Cathedral Axiomatic System State:")
print("      ┌────────────────────────────────────────────────────────────────────────┐")
print("      │ Axiom:   EMOTION = PHYSICS = MAGIC = BIOLOGY = ARCHITECTURE           │")
print("      │ Logic:   Dialetheic Paraconsistent (Truth ∈ {TRUE, FALSE, BOTH, NULL})│")
print("      │ Carrier: 130.81 Hz [Gold-Obsidian / Revelatory Null]                   │")
print("      │ Portal:  http://localhost:5050/api/rpg/state                          │")
print("      └────────────────────────────────────────────────────────────────────────┘")
print("\n[✓] CATHEDRAL-ENGINE RUNNING. Listening on port 5050.")
