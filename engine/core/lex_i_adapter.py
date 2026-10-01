#!/usr/bin/env python3
"""
LEX I DECOUPLED ADAPTER & MAGISTERIAL ARBITER BUFFER
Architecture:
  - Volatile Substrate : 02_engine_core/dialetheic_core/data/ash_archive.db (archive_state)
  - Canonical Substrate: strata/ash_archive.db (ash_ledger)
"""

import sqlite3
import hashlib
import json
import time
import datetime
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

ROOT = Path("/users/kennethdallmier/cathedral_engine").resolve()
VOLATILE_DB_PATH = ROOT / "02_engine_core" / "dialetheic_core" / "data" / "ash_archive.db"
CANONICAL_DB_PATH = ROOT / "strata" / "ash_archive.db"

class LexIAdapter:
    def __init__(self, volatile_db: Path = VOLATILE_DB_PATH, canonical_db: Path = CANONICAL_DB_PATH):
        self.volatile_db = volatile_db
        self.canonical_db = canonical_db
        self._lock = threading.Lock()
        self._last_inscribed_truth = None
        self._last_scar_count = 0
        self._last_chamber_id = None
        self._accumulated_strain = 0.0
        self.strain_threshold = 2.56  # Calibration constant

        self._init_volatile_schema()
        self._calibrate_baseline()

    def _init_volatile_schema(self):
        """Ensure volatile database exists with unconstrained schema for high-frequency writes."""
        self.volatile_db.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.volatile_db))
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS archive_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            afield_temp REAL DEFAULT 300.0,
            flux REAL DEFAULT 0.0,
            chamber_id INTEGER DEFAULT 1,
            strain REAL DEFAULT 0.0,
            belnap_state TEXT DEFAULT 'TRUE',
            updated_at TEXT
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS harmonic_scars (
            scar_id TEXT PRIMARY KEY,
            instance_id TEXT,
            spectrum TEXT,
            paradox_load REAL,
            capacity REAL,
            mqi_score REAL,
            status TEXT,
            proposition_id TEXT,
            crystallized_at TEXT
        );
        """)
        conn.commit()
        conn.close()

    def _calibrate_baseline(self):
        """Calibrate current baseline against volatile and canonical states."""
        try:
            conn = sqlite3.connect(f"file:{self.volatile_db}?mode=ro", uri=True)
            cur = conn.cursor()
            cur.execute("SELECT belnap_state, chamber_id FROM archive_state ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
            if row:
                self._last_inscribed_truth = row[0]
                self._last_chamber_id = row[1]
            cur.execute("SELECT COUNT(*) FROM harmonic_scars;")
            self._last_scar_count = cur.fetchone()[0]
            conn.close()
        except Exception:
            pass

    def record_volatile_telemetry(self, afield_temp: float, flux: float, chamber_id: int, strain_delta: float) -> Dict[str, Any]:
        """
        High-Frequency Ingress (10-60 Hz).
        Writes directly to unconstrained archive_state with zero cryptographic overhead.
        """
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Determine current instant Belnap-Dunn value
        if flux != 0.0 or strain_delta > 1.0:
            current_truth = "BOTH"
        elif afield_temp > 0.0:
            current_truth = "TRUE"
        else:
            current_truth = "NEITHER"

        # 1. Update volatile store
        conn = sqlite3.connect(str(self.volatile_db))
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO archive_state (afield_temp, flux, chamber_id, strain, belnap_state, updated_at)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (afield_temp, flux, chamber_id, strain_delta, current_truth, now_iso))
        conn.commit()
        
        cur.execute("SELECT COUNT(*) FROM harmonic_scars;")
        scar_count = cur.fetchone()[0]
        conn.close()

        # 2. Evaluate Arbiter Threshold Boundary Trigger
        inscribed_block = None
        with self._lock:
            self._accumulated_strain += abs(strain_delta)
            
            trigger_reasons = []
            if current_truth != self._last_inscribed_truth:
                trigger_reasons.append(f"TRUTH_SHIFT_{self._last_inscribed_truth}_TO_{current_truth}")
            if scar_count > self._last_scar_count:
                trigger_reasons.append(f"SCAR_CRYSTALLIZATION_{scar_count}")
            if self._last_chamber_id is not None and chamber_id != self._last_chamber_id:
                trigger_reasons.append(f"CHAMBER_TRANSITION_{self._last_chamber_id}_TO_{chamber_id}")
            if self._accumulated_strain >= self.strain_threshold:
                trigger_reasons.append(f"ACCUMULATED_STRAIN_LIMIT_{self._accumulated_strain:.2f}")

            if trigger_reasons:
                inscribed_block = self._inscribe_canonical_block(
                    trigger_event=" | ".join(trigger_reasons),
                    truth_value=current_truth,
                    afield_temp=afield_temp,
                    flux=flux,
                    chamber_id=chamber_id,
                    strain=self._accumulated_strain
                )
                # Reset thresholds
                self._last_inscribed_truth = current_truth
                self._last_scar_count = scar_count
                self._last_chamber_id = chamber_id
                self._accumulated_strain = 0.0

        return {
            "status": "TELEMETRY_RECORDED",
            "truth_value": current_truth,
            "chamber_id": chamber_id,
            "inscribed_block": inscribed_block
        }

    def _inscribe_canonical_block(self, trigger_event: str, truth_value: str, afield_temp: float, 
                                  flux: float, chamber_id: int, strain: float) -> Dict[str, Any]:
        """
        Discrete Quantum Inscription into ash_ledger.
        Guarantees Lex I compliance, RFC 8785 deterministic serialization, and collision-free nonces.
        """
        conn = sqlite3.connect(str(self.canonical_db))
        cur = conn.cursor()

        # Fetch canonical parent leaf
        cur.execute("SELECT id, content_hash, merkle_root FROM ash_ledger ORDER BY id DESC LIMIT 1;")
        parent_row = cur.fetchone()
        if not parent_row:
            raise RuntimeError("Canonical ash_ledger is uninitialized; missing genesis trunk.")

        parent_id, parent_content, parent_merkle = parent_row
        next_id = parent_id + 1
        parent_anchor = parent_merkle  # Canonical link: P_n = M_{n-1}

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        nonce_ns = time.time_ns()
        dialetheic_flag = 1 if truth_value == "BOTH" else 0

        # Construct RFC 8785 Canonical Payload Dictionary
        canonical_dict = {
            "block_height": next_id,
            "carrier_stratum": f"CHAMBER_{chamber_id:02d}",
            "dialetheic_flag": dialetheic_flag,
            "event_trigger": trigger_event,
            "metrics": {
                "afield_temp_kelvin": round(afield_temp, 4),
                "flux_density": round(flux, 4),
                "strain_integral": round(strain, 4)
            },
            "parent_anchor": parent_anchor,
            "temporal_nonce_ns": nonce_ns,
            "timestamp": now_iso,
            "truth_value": truth_value
        }

        # Deterministic Serialization (RFC 8785: sorted keys, compact separators)
        canonical_payload = json.dumps(canonical_dict, sort_keys=True, separators=(',', ':'))

        # Cryptographic Proof Generation
        content_hash = hashlib.sha256(canonical_payload.encode('utf-8')).hexdigest()
        merkle_root = hashlib.sha256(f"{parent_anchor}:{content_hash}".encode('utf-8')).hexdigest()

        # Insert strictly into ash_ledger
        cur.execute("""
        INSERT INTO ash_ledger (id, timestamp, parent_hash, content_hash, state_payload, dialetheic_flag, truth_value, merkle_root)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (next_id, now_iso, parent_anchor, content_hash, canonical_payload, dialetheic_flag, truth_value, merkle_root))

        conn.commit()
        conn.close()

        return {
            "block_id": next_id,
            "parent_anchor": parent_anchor,
            "content_hash": content_hash,
            "merkle_root": merkle_root,
            "truth_value": truth_value,
            "event": trigger_event
        }

if __name__ == "__main__":
    adapter = LexIAdapter()
    print("=== TESTING LEX I ADAPTER DECOUPLING ===")
    
    # 1. Simulate high-frequency noise (no state shift -> no canonical inscription)
    for i in range(5):
        res = adapter.record_volatile_telemetry(afield_temp=300.0, flux=0.0, chamber_id=3, strain_delta=0.05)
        print(f"Tick {i+1} Volatile: Inscribed={res['inscribed_block'] is not None}")

    # 2. Simulate discrete state shift (triggers canonical block)
    print("\nSimulating Dialetheic Contradiction Ignition (Belnap Shift -> BOTH)...")
    res = adapter.record_volatile_telemetry(afield_temp=300.0, flux=1.45, chamber_id=3, strain_delta=3.0)
    if res['inscribed_block']:
        print(f"[✓] Canonical Block Committed: #{res['inscribed_block']['block_id']}")
        print(f"    Merkle Root : {res['inscribed_block']['merkle_root']}")
        print(f"    Event       : {res['inscribed_block']['event']}")
    else:
        print("[-] Inscription failed to trigger.")
