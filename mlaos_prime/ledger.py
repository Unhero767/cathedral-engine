"""
ledger.py - Cryptographic Append-Only Merkle DAG Ledger
"""
import sqlite3
import hashlib
import json
import time
from typing import Dict, Any, List, Optional

class AshArchive:
    """Immutable ledger enforcing Lex I (dH/dt > 0)."""
    
    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self, db_path: str = "ash_archive.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blocks (
                    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL NOT NULL,
                    payload TEXT NOT NULL,
                    parent_hash TEXT NOT NULL,
                    block_hash TEXT NOT NULL UNIQUE
                )
            """)
            # Lex I Enforcers: Abort any modification or deletion
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS enforce_lex_i_no_update
                BEFORE UPDATE ON blocks
                BEGIN
                    SELECT RAISE(FAIL, 'Lex I Violation: Overwriting existing archive states is forbidden.');
                END;
            """)
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS enforce_lex_i_no_delete
                BEFORE DELETE ON blocks
                BEGIN
                    SELECT RAISE(FAIL, 'Lex I Violation: Deleting archive states is forbidden.');
                END;
            """)
            conn.commit()
        
        if self.get_height() == 0:
            self._mint_genesis()

    def _mint_genesis(self):
        payload = {"event": "GENESIS_INSCRIPTION", "location": "Olney, IL", "somatic_freq_hz": 1.5}
        self.append(payload, parent_hash_override=self.GENESIS_HASH)

    def get_last_block(self) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT index_id, timestamp, payload, parent_hash, block_hash FROM blocks ORDER BY index_id DESC LIMIT 1")
            row = cursor.fetchone()
            if not row:
                return None
            return {"index": row[0], "timestamp": row[1], "payload": json.loads(row[2]), "parent_hash": row[3], "block_hash": row[4]}

    def get_height(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM blocks")
            return cursor.fetchone()[0]

    def append(self, payload: Dict[str, Any], parent_hash_override: Optional[str] = None) -> str:
        last = self.get_last_block()
        parent_hash = parent_hash_override or (last["block_hash"] if last else self.GENESIS_HASH)
        
        ts = time.time()
        serialized_payload = json.dumps(payload, sort_keys=True)
        
        header = f"{ts}:{serialized_payload}:{parent_hash}"
        block_hash = hashlib.sha256(header.encode('utf-8')).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO blocks (timestamp, payload, parent_hash, block_hash) VALUES (?, ?, ?, ?)",
                (ts, serialized_payload, parent_hash, block_hash)
            )
            conn.commit()
            
        return block_hash

    def verify_integrity(self) -> bool:
        """Traverses the DAG to verify cryptographic continuity and Lex I validity."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT index_id, timestamp, payload, parent_hash, block_hash FROM blocks ORDER BY index_id ASC")
            rows = cursor.fetchall()
            
        if not rows:
            return False
            
        expected_parent = self.GENESIS_HASH
        for row in rows:
            idx, ts, payload_str, parent_hash, block_hash = row
            if parent_hash != expected_parent:
                return False
            
            header = f"{ts}:{payload_str}:{parent_hash}"
            computed_hash = hashlib.sha256(header.encode('utf-8')).hexdigest()
            if computed_hash != block_hash:
                return False
            
            expected_parent = block_hash
        return True
