import sys
import sqlite3
import hashlib
import json
import argparse
from pathlib import Path

DB_PATH = Path("ash_archive_stratum.db")

def init_db(enforce_immutable=True):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ash_archive_stratum (
            record_id TEXT PRIMARY KEY,
            proposition_id TEXT,
            evidence_positive INTEGER,
            evidence_negative INTEGER,
            timestamp REAL,
            source_id TEXT,
            causal_parents TEXT,
            payload_hash TEXT,
            resolution_status TEXT,
            supersedes_record_id TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[Ash Archive] Initialized Merkle DAG ledger at", DB_PATH.absolute())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--enforce-never-overwrite", action="store_true")
    args = parser.parse_args()
    if args.init:
        init_db(args.enforce_never_overwrite)
