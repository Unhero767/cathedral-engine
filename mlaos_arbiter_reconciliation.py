import sqlite3
import hashlib
import time

def reconcile_fracture_nodes():
    conn = sqlite3.connect("ash_archive.db")
    cursor = conn.cursor()
    
    # Ensure ledger table exists with Merkle DAG lineage fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ash_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            node_type TEXT,
            state_payload TEXT,
            parent_hash TEXT,
            current_hash TEXT
        )
    ''')
    
    timestamp = time.time()
    payload = "LEX_I_COMPLIANCE: Paraconsistent fracture node reconciled."
    
    # Fetch parent hash from the latest entry
    cursor.execute("SELECT current_hash FROM ash_ledger ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    parent_hash = row[0] if row else "0" * 64
    
    # Compute SHA-256 hash lineage
    raw_data = f"{timestamp}{payload}{parent_hash}"
    current_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    cursor.execute('''
        INSERT INTO ash_ledger (timestamp, node_type, state_payload, parent_hash, current_hash)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, "RECONCILIATION_NODE", payload, parent_hash, current_hash))
    
    conn.commit()
    conn.close()
    print(f"[MAGISTERIAL ARBITER] Synthesis block committed successfully.")
    print(f" -> Hash Lineage: {current_hash[:16]}...")

if __name__ == "__main__":
    reconcile_fracture_nodes()
