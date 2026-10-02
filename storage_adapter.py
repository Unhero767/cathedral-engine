#!/usr/bin/env python3
"""
StorageAdapter Interface & Implementations for Cathedral-Engine / MLAOS-Prime
=============================================================================
Specification: Lex I (The Never-Overwrite Doctrine: dH/dt > 0)
Sprint 01: Days 1–3 State Machine & Storage Decoupling
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time
from typing import Any, Dict, List, Optional

GENESIS_HASH: str = "0" * 64

class LexIViolationError(Exception):
    """Raised when an operation attempts to violate Lex I (Never-Overwrite)."""
    pass

class StorageAdapter(ABC):
    """Abstract storage interface decoupling state machine from persistence."""

    @abstractmethod
    def append_block(self, block_data: Dict[str, Any]) -> str:
        """Append a validated block to the immutable ledger. Returns block hash."""
        pass

    @abstractmethod
    def get_latest_hash(self) -> str:
        """Return the current tip hash of the ledger."""
        pass

    @abstractmethod
    def get_total_blocks(self) -> int:
        """Return the total number of blocks in the ledger."""
        pass

    @abstractmethod
    def read_range(self, start_height: int = 0, end_height: Optional[int] = None) -> List[Dict[str, Any]]:
        """Read a range of historical blocks [start_height, end_height]."""
        pass


class InMemoryAshArchive(StorageAdapter):
    """Pure in-memory mock storage for high-speed deterministic testing."""

    def __init__(self) -> None:
        self._blocks: List[Dict[str, Any]] = []
        self._tip_hash: str = GENESIS_HASH

    def append_block(self, block_data: Dict[str, Any]) -> str:
        height = len(self._blocks)
        parent_hash = block_data.get("parent_hash", self._tip_hash)
        if parent_hash != self._tip_hash:
            raise LexIViolationError(
                f"Parent hash mismatch! Expected {self._tip_hash}, got {parent_hash}"
            )

        raw_delta = block_data.get("state_delta") or block_data.get("delta") or {}
        if isinstance(raw_delta, str):
            try:
                delta_obj = json.loads(raw_delta)
            except Exception:
                delta_obj = raw_delta
        else:
            delta_obj = raw_delta

        cum_digest = str(block_data.get("cumulative_digest") or block_data.get("cum_digest") or "")
        ts = float(block_data.get("timestamp", time.time()))

        # Canonical hashing payload synchronized with verify_ash_dag.py
        payload = {
            "height": height,
            "parent": parent_hash,
            "delta": delta_obj,
            "cum_digest": cum_digest,
        }
        raw_canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        block_hash = hashlib.sha256(raw_canonical).hexdigest()

        record = {
            "height": height,
            "block_hash": block_hash,
            "parent_hash": parent_hash,
            "timestamp": ts,
            "state_delta": delta_obj,
            "cumulative_digest": cum_digest,
        }
        self._blocks.append(record)
        self._tip_hash = block_hash
        return block_hash

    def get_latest_hash(self) -> str:
        return self._tip_hash

    def get_total_blocks(self) -> int:
        return len(self._blocks)

    def read_range(self, start_height: int = 0, end_height: Optional[int] = None) -> List[Dict[str, Any]]:
        if end_height is None:
            return [dict(b) for b in self._blocks[start_height:]]
        return [dict(b) for b in self._blocks[start_height:end_height + 1]]


class SQLiteAshArchive(StorageAdapter):
    """Production SQLite storage engine enforcing WAL mode and Lex I triggers."""

    def __init__(self, db_path: Optional[Path] = None, table_name: str = "blocks") -> None:
        self.table_name = table_name
        self.db_path = self._resolve_db_path(db_path)
        self._init_database()

    def _resolve_db_path(self, explicit_path: Optional[Path]) -> Path:
        if explicit_path:
            target = explicit_path
        elif os.environ.get("ASH_ARCHIVE_DB"):
            target = Path(os.environ["ASH_ARCHIVE_DB"])
        elif os.environ.get("MLAOS_DATA_DIR"):
            data_dir = Path(os.environ["MLAOS_DATA_DIR"])
            data_dir.mkdir(parents=True, exist_ok=True)
            target = data_dir / "mla_ash_archive.db"
        else:
            temp_dir = Path(tempfile.gettempdir())
            target = temp_dir / "mla_ash_archive_ephemeral.db"

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            test_conn = sqlite3.connect(target)
            test_conn.close()
            return target
        except (sqlite3.OperationalError, PermissionError):
            fallback = Path(tempfile.gettempdir()) / f"ash_fallback_{int(time.time())}.db"
            return fallback

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_database(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    height INTEGER PRIMARY KEY,
                    block_hash TEXT NOT NULL UNIQUE,
                    parent_hash TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    state_delta TEXT NOT NULL,
                    cumulative_digest TEXT NOT NULL
                );
            """)
            cursor.execute(f"""
                CREATE TRIGGER IF NOT EXISTS prevent_{self.table_name}_update
                BEFORE UPDATE ON {self.table_name}
                BEGIN
                    SELECT RAISE(ABORT, 'LexIViolationError: In-place state modification strictly forbidden under Lex I (dH/dt > 0)');
                END;
            """)
            cursor.execute(f"""
                CREATE TRIGGER IF NOT EXISTS prevent_{self.table_name}_delete
                BEFORE DELETE ON {self.table_name}
                BEGIN
                    SELECT RAISE(ABORT, 'LexIViolationError: State record deletion strictly forbidden under Lex I (dH/dt > 0)');
                END;
            """)
            conn.commit()

    def append_block(self, block_data: Dict[str, Any]) -> str:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT height, block_hash FROM {self.table_name} ORDER BY height DESC LIMIT 1;")
            row = cursor.fetchone()
            if row:
                current_height = row["height"] + 1
                tip_hash = row["block_hash"]
            else:
                current_height = 0
                tip_hash = GENESIS_HASH

            parent_hash = block_data.get("parent_hash", tip_hash)
            if parent_hash != tip_hash:
                raise LexIViolationError(
                    f"Parent hash mismatch! Expected {tip_hash}, got {parent_hash}"
                )

            ts = float(block_data.get("timestamp", time.time()))
            raw_delta = block_data.get("state_delta") or block_data.get("delta") or {}
            if isinstance(raw_delta, str):
                try:
                    delta_obj = json.loads(raw_delta)
                except Exception:
                    delta_obj = raw_delta
                delta_json = raw_delta
            else:
                delta_obj = raw_delta
                delta_json = json.dumps(raw_delta, sort_keys=True)

            cum_digest = str(block_data.get("cumulative_digest") or block_data.get("cum_digest") or "")

            # Canonical hashing payload synchronized with verify_ash_dag.py
            payload = {
                "height": current_height,
                "parent": parent_hash,
                "delta": delta_obj,
                "cum_digest": cum_digest,
            }
            raw_canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            block_hash = hashlib.sha256(raw_canonical).hexdigest()

            cursor.execute(f"""
                INSERT INTO {self.table_name} (height, block_hash, parent_hash, timestamp, state_delta, cumulative_digest)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (current_height, block_hash, parent_hash, ts, delta_json, cum_digest))
            conn.commit()
            return block_hash

    def get_latest_hash(self) -> str:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT block_hash FROM {self.table_name} ORDER BY height DESC LIMIT 1;")
            row = cursor.fetchone()
            return row["block_hash"] if row else GENESIS_HASH

    def get_total_blocks(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name};")
            return cursor.fetchone()[0]

    def read_range(self, start_height: int = 0, end_height: Optional[int] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if end_height is None:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE height >= ? ORDER BY height ASC;", (start_height,))
            else:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE height >= ? AND height <= ? ORDER BY height ASC;", (start_height, end_height))
            return [dict(r) for r in cursor.fetchall()]
