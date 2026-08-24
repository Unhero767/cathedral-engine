import sqlite3
import hashlib
import json
import os

DB_PATH = os.path.join("strata", "ash_archive.db")

print("====================================================================================================")
print("             ASH ARCHIVE STRATA — END-TO-END CRYPTOGRAPHIC AUDIT & MERKLE PROOF                     ")
print("====================================================================================================")

if not os.path.exists(DB_PATH):
    print(f"[-] Database file missing at: {DB_PATH}")
    exit(1)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("""
    SELECT id, timestamp, parent_hash, content_hash, state_payload, 
           dialetheic_flag, truth_value, merkle_root
    FROM ash_ledger
    ORDER BY id ASC;
""")
blocks = c.fetchall()

print(f"\n[+] Total Ledger Blocks: {len(blocks)}\n")

chain_ok = True
merkle_ok = True

print(f"{'ID':<4} | {'Timestamp':<24} | {'Truth':<7} | {'Dialetheic':<10} | {'Content Hash':<16} | {'Merkle Root':<16} | {'Event / Construct'}")
print("-" * 118)

for idx, b in enumerate(blocks):
    b_id = b["id"]
    ts = b["timestamp"]
    parent = b["parent_hash"]
    c_hash = b["content_hash"]
    payload_str = b["state_payload"]
    dialetheic = b["dialetheic_flag"]
    truth = b["truth_value"]
    m_root = b["merkle_root"]
    
    # Parse payload event
    try:
        payload_json = json.loads(payload_str)
        event_name = payload_json.get("event", payload_json.get("action", "STATE_RECORD"))
        construct_name = payload_json.get("construct_name", payload_json.get("construct", ""))
        descriptor = f"{event_name} [{construct_name}]" if construct_name else event_name
    except Exception:
        descriptor = "RAW_PAYLOAD"

    # Verify SHA-256(parent:payload:ts)
    calc_content = hashlib.sha256(f"{parent}:{payload_str}:{ts}".encode("utf-8")).hexdigest()
    # Verify SHA-256(content:ts)
    calc_merkle = hashlib.sha256(f"{c_hash}:{ts}".encode("utf-8")).hexdigest()
    
    if idx > 0 and parent != blocks[idx - 1]["content_hash"]:
        chain_ok = False
    if calc_content != c_hash:
        chain_ok = False
    if m_root and calc_merkle != m_root:
        merkle_ok = False
        
    print(f"{b_id:<4} | {ts[:23]:<24} | {str(truth):<7} | {str(dialetheic):<10} | {c_hash[:16]:<16} | {m_root[:16]:<16} | {descriptor[:34]}")

print("-" * 118)

if chain_ok and merkle_ok:
    print("\n[✓] CRYPTOGRAPHIC INTEGRITY: 100% VERIFIED — ALL LEDGER BLOCKS & MERKLE ROOTS IMMUTABLE & VALID.")
else:
    print(f"\n[!] INTEGRITY ALERT — Chain Valid: {chain_ok} | Merkle Valid: {merkle_ok}")

print("\n====================================================================================================")
print("                           SANGUINE HEURISTIC SCARS (COLLISION MATRIX)                              ")
print("====================================================================================================")

c.execute("""
    SELECT id, timestamp, scar_hash, source_collision_type, routing_adjustment, merkle_ref
    FROM sanguine_heuristics
    ORDER BY id ASC;
""")
scars = c.fetchall()

print(f"[+] Total Sanguine Scars: {len(scars)}\n")
for s in scars:
    print(f"• Scar #{s['id']:02d} [{s['scar_hash'][:16]}...] | Collision: {s['source_collision_type']}")
    print(f"    Merkle Ref: {s['merkle_ref'][:24]}...")
    print(f"    Adjustment: {s['routing_adjustment']}")

print("\n====================================================================================================")
print("                              FINAL ARCHITECT TELEMETRY & STRATA STATE                               ")
print("====================================================================================================")

c.execute("SELECT * FROM player_state WHERE player_id = 'player_primary';")
p = c.fetchone()
if p:
    print(f"• Sovereign ID:      {p['player_id']}")
    print(f"• Current Chamber:   Chamber {p['current_chamber_id']} (Sanctum Apex / Core Monad)")
    print(f"• Coordinates:       ({p['coord_x']}, {p['coord_y']}) [Transcendence Oculus]")
    print(f"• Harmonic Spectrum: {p['active_spectrum']}")
    print(f"• Final Sync:        {p['last_updated']}")

conn.close()
