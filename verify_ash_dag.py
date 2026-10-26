#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path('ash_archive.db')

def verify_dag():
    if not DB_PATH.exists():
        print(f'[ERROR] Database {DB_PATH} not found.')
        return False
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, timestamp, node_type, parent_hash, current_hash, merkle_leaf_hash FROM ash_ledger ORDER BY id ASC;")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print('[WARNING] Ash Archive ledger is empty.')
        return False
        
    print("=" * 80)
    print(" CATHEDRAL-ENGINE // ASH ARCHIVE MERKLE DAG LINEAGE VERIFICATION")
    print("=" * 80)
    
    prev_hash = None
    for row in rows:
        idx, ts, node_type, parent, current_hash, leaf = row
        print(f"[{idx:02d}] {ts} | Type: {node_type}")
        print(f"     -> Parent Hash:  {parent}")
        print(f"     -> Current Hash: {current_hash}")
        print(f"     -> Merkle Leaf:  {leaf}")
        
        if prev_hash is not None and parent != prev_hash:
            print(f"     [!] LINEAGE BREAK DETECTED: Parent {parent} does not match previous hash {prev_hash}")
            return False
        else:
            print(f"     [✓] Lineage Link Verified")
            
        prev_hash = current_hash
        print("-" * 80)
        
    print(f"SUCCESS: All {len(rows)} ledger nodes verified with unbroken Merkle lineage.")
    print("=" * 80)
    return True

if __name__ == '__main__':
    verify_dag()
