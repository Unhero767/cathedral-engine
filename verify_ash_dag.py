#!/usr/bin/env python3
"""
Ash Archive Merkle DAG Lineage Verifier (Stratum I & II)
Author: Kenneth Wayne Dallmier (Dallmier Tech Venture, Olney, IL)
Governing Doctrine: Lex I (Never-Overwrite) // Lex IV (Belnap-Dunn FOUR)
"""

import sqlite3
import hashlib
from pathlib import Path

DB_PATH = Path("ash_archive_stratum.db")

def verify_dag():
    if not DB_PATH.exists():
        print(f"[ERROR] Database {DB_PATH} not found.")
        return False
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, timestamp, chamber_designation, parent_hash, current_state_root, signature_hash FROM ash_dag_ledger ORDER BY id ASC;")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("[WARNING] Ash Archive ledger is empty.")
        return False
        
    print("=" * 80)
    print(" CATHEDRAL-ENGINE // ASH ARCHIVE MERKLE DAG LINEAGE VERIFICATION")
    print("=" * 80)
    
    prev_root = None
    for row in rows:
        idx, ts, chamber, parent, current_root, sig = row
        print(f"[{idx:02d}] {ts} | {chamber}")
        print(f"     -> Parent Hash:  {parent}")
        print(f"     -> State Root:   {current_root}")
        print(f"     -> Signature:    {sig}")
        
        if prev_root is not None and parent != prev_root:
            print(f"     [!] LINEAGE BREAK DETECTED: Parent {parent} does not match previous root {prev_root}")
            return False
        else:
            print(f"     [✓] Lineage Link Verified")
            
        prev_root = current_root
        print("-" * 80)
        
    print(f"SUCCESS: All {len(rows)} ledger nodes verified with unbroken Merkle lineage.")
    print("=" * 80)
    return True

if __name__ == "__main__":
    verify_dag()
