#!/usr/bin/env python3
"""
Commit consolidated telemetry stratum into ash_ledger under Lex I lineage.
"""

import hashlib, json, sqlite3, time
from pathlib import Path

db_path = Path("./ash_archive.db").resolve()
conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

# Retrieve current Merkle Tip
cur.execute("SELECT id, current_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
last_row = cur.fetchone()
if not last_row:
    print("Error: No genesis block found in ash_ledger.")
    conn.close()
    exit(1)

last_id, parent_hash = last_row
next_id = last_id + 1
now_epoch = time.time()

# Compute cumulative hash over all 112 experiment records
cur.execute("SELECT merkle_hash FROM lab_experiments ORDER BY id ASC;")
hashes = [r[0] for r in cur.fetchall()]
composite_digest = hashlib.sha256("".join(hashes).encode("utf-8")).hexdigest()

payload_dict = {
    "stratum": "06_strata_data/prime_ledger.ndjson",
    "event_count": len(hashes),
    "spectral_dominant": "Bronze-Obsidian/Null",
    "dialetheic_state": "Both",
    "composite_digest": composite_digest
}
payload_json = json.dumps(payload_dict, sort_keys=True, separators=(",", ":"))

# Block hash = SHA256(next_id + now_epoch + node_type + payload + parent_hash)
block_header = f"{next_id}:{now_epoch}:RECONCILIATION_NODE:{payload_json}:{parent_hash}"
current_hash = hashlib.sha256(block_header.encode("utf-8")).hexdigest()

cur.execute(
    """INSERT INTO ash_ledger (timestamp, node_type, state_payload, parent_hash, current_hash)
       VALUES (?, ?, ?, ?, ?);""",
    (now_epoch, "RECONCILIATION_NODE", payload_json, parent_hash, current_hash)
)

conn.commit()
conn.close()

print(f"Committed Block {next_id} -> Tip: {current_hash}")
