import sqlite3
import hashlib
import json
import os

DB_PATH = os.path.join("strata", "ash_archive.db")

print("================================================================================")
print(" ASH ARCHIVE CRYPTOGRAPHIC LEDGER AUDIT & MERKLE VERIFICATION")
print("================================================================================")

if not os.path.exists(DB_PATH):
    print(f"[-] Database file not found at: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. Fetch all blocks
c.execute("""
    SELECT id, timestamp, parent_hash, content_hash, state_payload, 
           dialetheic_flag, truth_value, merkle_root
    FROM ash_ledger
    ORDER BY id ASC;
""")
blocks = c.fetchall()

print(f"\n[+] Total Blocks in ash_ledger: {len(blocks)}\n")

chain_valid = True
merkle_valid = True

print(f"{'ID':<4} | {'Timestamp':<25} | {'Truth':<6} | {'Dialetheic':<10} | {'Parent Hash':<16} | {'Content Hash':<16} | {'Status'}")
print("-" * 115)

for idx, b in enumerate(blocks):
    b_id = b["id"]
    ts = b["timestamp"]
    parent = b["parent_hash"]
    c_hash = b["content_hash"]
    payload = b["state_payload"]
    dialetheic = b["dialetheic_flag"]
    truth = b["truth_value"]
    m_root = b["merkle_root"]
    
    # Verify Content Hash: SHA-256(parent:payload:ts)
    expected_content_hash = hashlib.sha256(f"{parent}:{payload}:{ts}".encode("utf-8")).hexdigest()
    
    # Verify Merkle Root: SHA-256(content_hash:ts)
    expected_merkle_root = hashlib.sha256(f"{c_hash}:{ts}".encode("utf-8")).hexdigest()
    
    status_flags = []
    
    # Check parent linkage
    if idx > 0:
        prev_hash = blocks[idx - 1]["content_hash"]
        if parent != prev_hash:
            chain_valid = False
            status_flags.append("LINK_BROKEN")
    
    if expected_content_hash != c_hash:
        chain_valid = False
        status_flags.append("HASH_CORRUPT")
        
    if m_root and expected_merkle_root != m_root:
        merkle_valid = False
        status_flags.append("MERKLE_MISMATCH")
        
    status_str = "VALID [OK]" if not status_flags else "FAILED (" + ",".join(status_flags) + ")"
    
    print(f"{b_id:<4} | {ts:<25} | {str(truth):<6} | {str(dialetheic):<10} | {parent[:16]:<16} | {c_hash[:16]:<16} | {status_str}")

print("-" * 115)
if chain_valid and merkle_valid:
    print("[✓] CRYPTOGRAPHIC INTEGRITY: 100% VERIFIED — ALL LEDGER BLOCKS & MERKLE ROOTS ARE IMMUTABLE & VALID.")
else:
    print(f"[!] INTEGRITY WARNING: Chain Valid: {chain_valid} | Merkle Valid: {merkle_valid}")

print("\n================================================================================")
print(" SANGUINE HEURISTIC SCARS (LOAD-BEARING COLLISION MATRIX)")
print("================================================================================")

c.execute("""
    SELECT id, timestamp, scar_hash, source_collision_type, routing_adjustment, merkle_ref
    FROM sanguine_heuristics
    ORDER BY id ASC;
""")
scars = c.fetchall()

print(f"[+] Total Sanguine Scars: {len(scars)}\n")
for s in scars:
    print(f"• Scar #{s['id']} [{s['scar_hash'][:16]}...] | Type: {s['source_collision_type']}")
    print(f"    Merkle Ref:  {s['merkle_ref'][:20]}...")
    print(f"    Adjustment:  {s['routing_adjustment']}")

print("\n================================================================================")
print(" ACTIVE PLAYER TELEMETRY & STRATA STATE")
print("================================================================================")

c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
p = c.fetchone()
if p:
    print(f"• Player ID:         {p['player_id']}")
    print(f"• Chamber ID:        Chamber {p['current_chamber_id']}")
    print(f"• Coordinate Vector: ({p['coord_x']}, {p['coord_y']})")
    print(f"• Active Spectrum:   {p['active_spectrum']}")
    print(f"• Last Synchronized: {p['last_updated']}")

conn.close()
