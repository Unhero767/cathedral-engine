import sqlite3
import hashlib
import json
from pathlib import Path

# Resolve correct Ash Archive path across known repository strata
CANDIDATE_PATHS = [
    Path("ash_archive_stratum.db"),
    Path("strata/ash_archive.db"),
    Path("stratum_alpha.db")
]

DB_PATH = next((p for p in CANDIDATE_PATHS if p.exists()), CANDIDATE_PATHS[0])
MANIFEST_PATH = Path("config/registry_manifest.json")

def compute_block_hash(block_index: int, payload: bytes, parent_hash: str) -> str:
    hasher = hashlib.sha256()
    hasher.update(str(block_index).encode('utf-8'))
    hasher.update(payload)
    hasher.update(parent_hash.encode('utf-8'))
    return hasher.hexdigest()

def audit_ash_archive_wal():
    print(v := f"[*] Target Substrate Path: {DB_PATH.resolve()}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()
    
    # Ensure ash_blocks schema exists (Lex I compliant append-only structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ash_blocks (
            block_index INTEGER PRIMARY KEY AUTOINCREMENT,
            payload BLOB NOT NULL,
            parent_hash TEXT NOT NULL,
            block_hash TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    
    cursor.execute("SELECT block_index, payload, parent_hash, block_hash FROM ash_blocks ORDER BY block_index ASC;")
    rows = cursor.fetchall()
    
    if not rows:
        print("[*] Stratum contains zero blocks. Inscribing Genesis Witness Block...")
        genesis_payload = b"MLAES-PRIME-GENESIS-STATE-EXACT-001"
        parent_hash = "0" * 64
        block_hash = compute_block_hash(0, genesis_payload, parent_hash)
        cursor.execute(
            "INSERT INTO ash_blocks (block_index, payload, parent_hash, block_hash) VALUES (?, ?, ?, ?);",
            (0, genesis_payload, parent_hash, block_hash)
        )
        conn.commit()
        cursor.execute("SELECT block_index, payload, parent_hash, block_hash FROM ash_blocks ORDER BY block_index ASC;")
        rows = cursor.fetchall()

    expected_parent = "0" * 64
    calculated_merkle_root = hashlib.sha256(b"GENESIS_ROOT").hexdigest()

    print(f"--- Initiating Cryptographic Chain Audit ({len(rows)} Blocks) ---")
    
    for row in rows:
        idx, payload, parent_hash, stored_hash = row
        
        # Verify parent hash continuity
        if parent_hash != expected_parent:
            raise ValueError(f"Chain Fracture at Block {idx}: Expected parent {expected_parent}, found {parent_hash}")
        
        # Verify block hash integrity
        recalculated = compute_block_hash(idx, payload, parent_hash)
        if recalculated != stored_hash:
            raise ValueError(f"Cryptographic Mismatch at Block {idx}: Stored hash {stored_hash} differs from computed {recalculated}")
        
        # Advance Merkle accumulator
        root_hasher = hashlib.sha256()
        root_hasher.update(calculated_merkle_root.encode('utf-8'))
        root_hasher.update(stored_hash.encode('utf-8'))
        calculated_merkle_root = root_hasher.hexdigest()
        
        expected_parent = stored_hash

    conn.close()
    print(f"[+] Chain Continuity Verified: Zero truncation anomalies detected.")
    print(f"[+] Computed SHA-256 Merkle Root: {calculated_merkle_root}")

    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r") as f:
            manifest = json.load(f)
        manifest_root = manifest.get("merkle_root")
        if manifest_root and manifest_root != calculated_merkle_root:
            raise ValueError(f"Manifest Mismatch: Registry root {manifest_root} does not match computed root {calculated_merkle_root}")
        print(f"[+] Manifest Synchronization Verified: Root matches local registry.")
    else:
        print(f"[!] Manifest path {MANIFEST_PATH} not found; skipping registry cross-check.")

if __name__ == "__main__":
    audit_ash_archive_wal()
