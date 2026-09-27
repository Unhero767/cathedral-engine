#!/usr/bin/env python3
import sqlite3
import hashlib
from pathlib import Path

DB_PATH = "ash_archive_stratum.db"

def verify_chain():
    print("==> Verifying Ash Archive Merkle Lineage Chain...")
    if not Path(DB_PATH).exists():
        print("ERROR: ash_archive_stratum.db not found. Run mlaos_convergence_seal.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, payload, parent_hash, merkle_hash, timestamp FROM ash_archive_stratum ORDER BY id ASC;")
    rows = cursor.fetchall()
    
    if not rows:
        print("==> Ash Archive is empty.")
        conn.close()
        return

    expected_parent = "0000000000000000000000000000000000000000000000000000000000000000"
    valid = True
    
    for row in rows:
        block_id, payload, parent_hash, merkle_hash, timestamp = row
        if parent_hash != expected_parent:
            print(f"  [FAIL] Block #{block_id}: Parent hash mismatch! Expected {expected_parent[:12]}..., Got {parent_hash[:12]}...")
            valid = False
            
        raw_data = f"{parent_hash}:{payload}:{timestamp}".encode('utf-8')
        computed_hash = hashlib.sha256(raw_data).hexdigest()
        
        if computed_hash != merkle_hash:
            print(f"  [FAIL] Block #{block_id}: Merkle hash tampering detected!")
            valid = False
        else:
            print(f"  [PASS] Block #{block_id} Verified -> {merkle_hash[:12]}...")
            
        expected_parent = merkle_hash

    conn.close()
    if valid:
        print("==> Merkle Lineage Chain Integrity: 100% VALID.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify_chain()
