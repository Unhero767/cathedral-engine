"""
Cathedral-Engine SQLite Database Manager.
Governs strata/ash_archive.db enforcing Never-Overwrite Doctrine and JBP Ledger.
"""

from __future__ import annotations
import sqlite3
import json
import time
import os
from typing import List, Dict, Optional, Tuple, Any
from .models import AshBlock, CodexBook, CodexChapter, OracleCard, Spectral

DB_PATH = "/working_dir/c_9a0a4a350cc893af/strata/ash_archive.db"

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = MEMORY;")
        conn.execute("PRAGMA synchronous = OFF;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Ash Archive JBP Merkle Ledger
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ash_ledger (
                block_index INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                parent_hash TEXT NOT NULL,
                block_hash TEXT NOT NULL UNIQUE,
                merkle_root TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                jbp_signature TEXT NOT NULL
            );
            """)

            # 2. 40-Book Codex Strata Registry
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS codex_strata (
                book_id INTEGER PRIMARY KEY,
                roman_numeral TEXT NOT NULL,
                title TEXT NOT NULL,
                tier_designation TEXT NOT NULL,
                tier_range TEXT NOT NULL,
                spectral_dominant TEXT NOT NULL,
                primary_axiom TEXT NOT NULL,
                isomorphism_bio TEXT NOT NULL,
                isomorphism_arch TEXT NOT NULL,
                isomorphism_math TEXT NOT NULL,
                parent_block_hash TEXT NOT NULL
            );
            """)

            # 3. 40-Book Codex Generated Chapters
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS codex_chapters (
                chapter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL REFERENCES codex_strata(book_id),
                chapter_designation TEXT NOT NULL,
                core_thesis TEXT NOT NULL,
                preceding_bridge TEXT NOT NULL,
                following_gateway TEXT NOT NULL,
                spectral_dominant_hz REAL NOT NULL,
                content_hash TEXT NOT NULL UNIQUE,
                merkle_proof TEXT NOT NULL,
                parent_ledger_hash TEXT NOT NULL,
                full_monograph TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            """)

            # 4. 377-Card Persona Oracle Deck Registry
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS oracle_deck_strata (
                card_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                arcana TEXT NOT NULL,
                tier_strata TEXT NOT NULL,
                spectral TEXT NOT NULL,
                tau_delta REAL NOT NULL,
                rho_delta REAL NOT NULL,
                delta_delta REAL NOT NULL,
                sigma_delta REAL NOT NULL,
                carrier_freq_hz REAL NOT NULL,
                flavour_lore TEXT NOT NULL
            );
            """)

            # 5. Engine State Telemetry History
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS engine_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turn INTEGER NOT NULL,
                tau_pol REAL NOT NULL,
                rho_res REAL NOT NULL,
                delta_fac REAL NOT NULL,
                sigma_coh REAL NOT NULL,
                carrier_hz REAL NOT NULL,
                flux_dphi_dt REAL NOT NULL,
                active_spectral TEXT NOT NULL,
                active_chamber_id INTEGER NOT NULL,
                timestamp REAL NOT NULL
            );
            """)
            conn.commit()

            # Ensure Genesis Block exists
            self._ensure_genesis_block(cursor, conn)

    def _ensure_genesis_block(self, cursor: sqlite3.Cursor, conn: sqlite3.Connection):
        cursor.execute("SELECT COUNT(*) FROM ash_ledger")
        if cursor.fetchone()[0] == 0:
            genesis = AshBlock(
                index=0,
                timestamp=time.time(),
                parent_hash="0" * 64,
                merkle_root="0" * 64,
                event_type="GENESIS_BLOCK",
                payload_json=json.dumps({"doctrine": "Never-Overwrite", "strata": "Books I–XL Genesis Locked", "carrier_hz": 130.81})
            )
            genesis.block_hash = genesis.calculate_hash()
            genesis.jbp_signature = genesis.generate_signature()
            
            cursor.execute("""
            INSERT INTO ash_ledger (block_index, timestamp, parent_hash, block_hash, merkle_root, event_type, payload_json, jbp_signature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (genesis.index, genesis.timestamp, genesis.parent_hash, genesis.block_hash, genesis.merkle_root, genesis.event_type, genesis.payload_json, genesis.jbp_signature))
            conn.commit()

    def append_ash_block(self, event_type: str, payload: Dict[str, Any], merkle_root: str = "") -> AshBlock:
        """Appends a new block to the Ash Archive under the Never-Overwrite Doctrine."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT block_index, block_hash FROM ash_ledger ORDER BY block_index DESC LIMIT 1")
            last_row = cursor.fetchone()
            last_idx = last_row["block_index"]
            last_hash = last_row["block_hash"]
            
            payload_str = json.dumps(payload, sort_keys=True)
            if not merkle_root:
                import hashlib
                merkle_root = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
                
            block = AshBlock(
                index=last_idx + 1,
                timestamp=time.time(),
                parent_hash=last_hash,
                merkle_root=merkle_root,
                event_type=event_type,
                payload_json=payload_str
            )
            block.block_hash = block.calculate_hash()
            block.jbp_signature = block.generate_signature()

            cursor.execute("""
            INSERT INTO ash_ledger (block_index, timestamp, parent_hash, block_hash, merkle_root, event_type, payload_json, jbp_signature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (block.index, block.timestamp, block.parent_hash, block.block_hash, block.merkle_root, block.event_type, block.payload_json, block.jbp_signature))
            conn.commit()
            return block

    def get_latest_ash_block(self) -> AshBlock:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ash_ledger ORDER BY block_index DESC LIMIT 1")
            row = cursor.fetchone()
            return AshBlock(
                index=row["block_index"],
                timestamp=row["timestamp"],
                parent_hash=row["parent_hash"],
                merkle_root=row["merkle_root"],
                event_type=row["event_type"],
                payload_json=row["payload_json"],
                block_hash=row["block_hash"],
                jbp_signature=row["jbp_signature"]
            )
