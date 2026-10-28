#!/usr/bin/env python3
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

DB_PATH = "ash_archive_stratum.db"

def seal_convergence():
    print("==> Initializing Ash Archive Convergence Seal...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ash_archive_stratum (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT NOT NULL,
            parent_hash TEXT NOT NULL,
            merkle_hash TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    
    # Get last block hash or genesis
    cursor.execute("SELECT merkle_hash FROM ash_archive_stratum ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    parent_hash = row[0] if row else "0000000000000000000000000000000000000000000000000000000000000000"
    
    payload = "Convergence Seal: MLAOS-Prime & Cathedral-Engine Stratum Synchronized under Lex I."
    timestamp = datetime.utcnow().isoformat()
    
    raw_data = f"{parent_hash}:{payload}:{timestamp}".encode('utf-8')
    merkle_hash = hashlib.sha256(raw_data).hexdigest()
    
    cursor.execute("""
        INSERT INTO ash_archive_stratum (payload, parent_hash, merkle_hash, timestamp)
        VALUES (?, ?, ?, ?)
    """, (payload, parent_hash, merkle_hash, timestamp))
    
    conn.commit()
    conn.close()
    print(f"==> Ash Archive Sealed Successfully | Merkle Hash: {merkle_hash[:16]}...")

if __name__ == "__main__":
    seal_convergence()
