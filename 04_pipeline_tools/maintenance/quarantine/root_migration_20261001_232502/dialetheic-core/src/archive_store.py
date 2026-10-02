# src/archive_store.py
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "data" / "ash_archive.db"

class ArchiveStore:
    def __init__(self, db_path: str = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._init_db()
        except sqlite3.OperationalError:
            fallback_dir = Path("/tmp/dialetheic_data")
            fallback_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = fallback_dir / "ash_archive.db"
            self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=10.0)

    def _init_db(self):
        """Carves the schema into the SQLite vault."""
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS archive_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS archive_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    afield_temp REAL,
                    flux REAL,
                    updated_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS harmonic_scars (
                    scar_id TEXT PRIMARY KEY,
                    instance_id TEXT,
                    spectrum TEXT,
                    paradox_load REAL,
                    capacity REAL,
                    mqi_score REAL,
                    status TEXT,
                    proposition_id TEXT,
                    proposition_text TEXT,
                    proposition_p TEXT,
                    created_at TEXT NOT NULL DEFAULT (datetime('now')),
                    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
                )
            """)
            cursor = conn.execute("PRAGMA table_info(harmonic_scars)")
            columns = [col[1] for col in cursor.fetchall()]
            if "mqi_score" not in columns:
                conn.execute("ALTER TABLE harmonic_scars ADD COLUMN mqi_score REAL")
            if "status" not in columns:
                conn.execute("ALTER TABLE harmonic_scars ADD COLUMN status TEXT")
            if "proposition_id" not in columns:
                conn.execute("ALTER TABLE harmonic_scars ADD COLUMN proposition_id TEXT")
            if "proposition_text" not in columns:
                conn.execute("ALTER TABLE harmonic_scars ADD COLUMN proposition_text TEXT")
            if "proposition_p" not in columns:
                conn.execute("ALTER TABLE harmonic_scars ADD COLUMN proposition_p TEXT")

            cursor = conn.execute("SELECT COUNT(*) FROM archive_state")
            if cursor.fetchone()[0] == 0:
                conn.execute("""
                    INSERT INTO archive_state (id, afield_temp, flux, updated_at)
                    VALUES (1, 300.0, 0.0, ?)
                """, (datetime.utcnow().isoformat(),))
            conn.commit()

    def set_meta(self, key: str, value: str):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO archive_meta (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value;
            """, (key, str(value)))
            conn.commit()

    def get_meta(self, key: str, default: Optional[str] = None) -> Optional[str]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM archive_meta WHERE key = ?;", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def get_state(self) -> dict:
        """Recalls the A-Field baseline."""
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM archive_state WHERE id = 1").fetchone()
            if row:
                return {
                    "afield_temp": row["afield_temp"],
                    "flux": row["flux"]
                }
            return {"afield_temp": 300.0, "flux": 0.0}

    def save_state(self, afield_temp: float, flux: float):
        """Seals the current A-Field metrics into the vault."""
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE archive_state 
                SET afield_temp = ?, flux = ?, updated_at = ?
                WHERE id = 1
            """, (afield_temp, flux, datetime.utcnow().isoformat()))
            conn.commit()

    def get_scars(self) -> list[dict]:
        """Resurrects all active Harmonic Scars."""
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM harmonic_scars").fetchall()
            return [dict(r) for r in rows]

    def get_all_scars(self) -> list[dict]:
        """Alias for get_scars()."""
        return self.get_scars()

    def upsert_scar(self, scar: dict, instance_id: Optional[str] = None):
        """Binds a new or updated scar into the permanent record."""
        scar_id = scar.get("scar_id") or scar.get("instance_id") or "scar_unknown"
        node_instance_id = instance_id or scar.get("instance_id") or "AURELIA-NODE"
        spectrum = scar.get("spectrum") or scar.get("active_spectrum") or "TEAL"
        
        paradox_load = scar.get("paradox_load")
        if paradox_load is None:
            paradox_load = scar.get("active_paradox_load")
        if paradox_load is None:
            paradox_load = scar.get("contradiction_degree", 0.0)
        paradox_load = float(paradox_load)

        capacity = float(scar.get("capacity") or scar.get("load_bearing_capacity", 0.0))
        mqi_score = scar.get("mqi_score")
        status_val = scar.get("status") or scar.get("action")
        proposition_id = scar.get("proposition_id") or scar.get("verse_id")
        proposition_text = scar.get("proposition_text") or scar.get("proposition_p") or scar.get("claim") or "No proposition text"
        now = datetime.utcnow().isoformat()

        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO harmonic_scars 
                (scar_id, instance_id, spectrum, paradox_load, capacity, mqi_score, status, proposition_id, proposition_text, proposition_p, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(scar_id) DO UPDATE SET
                    instance_id=excluded.instance_id,
                    spectrum=excluded.spectrum,
                    paradox_load=excluded.paradox_load,
                    capacity=excluded.capacity,
                    mqi_score=excluded.mqi_score,
                    status=excluded.status,
                    proposition_id=excluded.proposition_id,
                    proposition_text=excluded.proposition_text,
                    proposition_p=excluded.proposition_p,
                    updated_at=excluded.updated_at
            """, (
                scar_id,
                node_instance_id,
                spectrum,
                paradox_load,
                capacity,
                mqi_score,
                status_val,
                proposition_id,
                proposition_text,
                proposition_text,
                now,
                now
            ))
            conn.commit()
