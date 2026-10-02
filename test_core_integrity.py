#!/usr/bin/env python3
"""
Test Core Integrity (test_core_integrity.py)
============================================
Sprint 01 Verification Harness for Gates 01 & 02
Checks: State machine determinism, Lex I database triggers, Belnap-Dunn dialetheic logic, 
        DAG hash-chain verification, and 119-element strata distribution.
"""
from pathlib import Path
import sqlite3
import tempfile
import unittest

from storage_adapter import InMemoryAshArchive, SQLiteAshArchive, LexIViolationError
from mlaos_engine_core import MLAOSCognitiveEngine, BelnapValue
from verify_ash_dag import AshLedgerVerifier, CANONICAL_ZONES

class TestStorageAdapterIntegrity(unittest.TestCase):
    def test_in_memory_monotonic_append(self):
        archive = InMemoryAshArchive()
        h0 = archive.append_block({"state_delta": {"init": True}, "timestamp": 100.0})
        h1 = archive.append_block({"state_delta": {"tick": 1}, "parent_hash": h0, "timestamp": 100.666})
        self.assertEqual(archive.get_total_blocks(), 2)
        self.assertEqual(archive.get_latest_hash(), h1)

        with self.assertRaises(LexIViolationError):
            archive.append_block({"state_delta": {"bad": True}, "parent_hash": "invalid_parent"})

    def test_sqlite_lex_i_triggers(self):
        temp_db = Path(tempfile.gettempdir()) / "test_lex_i.db"
        if temp_db.exists():
            temp_db.unlink()

        archive = SQLiteAshArchive(db_path=temp_db)
        h0 = archive.append_block({"state_delta": {"init": True}, "timestamp": 100.0})
        h1 = archive.append_block({"state_delta": {"tick": 1}, "parent_hash": h0, "timestamp": 100.667})

        self.assertEqual(archive.get_total_blocks(), 2)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        with self.assertRaises((sqlite3.IntegrityError, sqlite3.OperationalError)):
            cursor.execute("UPDATE blocks SET timestamp = 999.0 WHERE height = 0;")
        with self.assertRaises((sqlite3.IntegrityError, sqlite3.OperationalError)):
            cursor.execute("DELETE FROM blocks WHERE height = 0;")
        conn.close()

class TestMLAOSStateMachine(unittest.TestCase):
    def test_pure_transition_and_scar_crystallization(self):
        storage = InMemoryAshArchive()
        engine = MLAOSCognitiveEngine(storage=storage)

        resolved = engine.process_dialetheic_input("threshold_breached", assert_true=True, assert_false=True)
        self.assertEqual(resolved, BelnapValue.B)
        self.assertEqual(len(engine.state.scars), 0)

        engine.process_dialetheic_input("secondary_tension", assert_true=True, assert_false=True)
        self.assertEqual(len(engine.state.scars), 1)
        scar = engine.state.scars[0]
        self.assertAlmostEqual(scar.shear_angle_deg, 54.7356, places=3)

        m1 = engine.transition({"chamber_status": "LITHIC_SEALED"})
        self.assertEqual(m1.S["chamber_status"], "LITHIC_SEALED")
        self.assertEqual(storage.get_total_blocks(), 1)

class TestVerifierDAG(unittest.TestCase):
    def test_verifier_end_to_end(self):
        temp_db = Path(tempfile.gettempdir()) / "test_verifier.db"
        if temp_db.exists():
            temp_db.unlink()

        archive = SQLiteAshArchive(db_path=temp_db)
        h0 = archive.append_block({"state_delta": {"step": 0}, "timestamp": 100.0})
        h1 = archive.append_block({"state_delta": {"step": 1}, "parent_hash": h0, "timestamp": 100.667})
        h2 = archive.append_block({"state_delta": {"step": 2}, "parent_hash": h1, "timestamp": 101.334})

        verifier = AshLedgerVerifier()
        verifier.load_sqlite(temp_db, table_name="blocks")
        report = verifier.verify_dag(strict_pulse=True)

        self.assertEqual(report["status"], "VERIFIED")
        self.assertEqual(report["total_blocks"], 3)
        self.assertEqual(report["violations_count"], 0)

        cert = verifier.generate_certificate(str(temp_db), report)
        self.assertEqual(cert["attestation_status"], "VERIFIED")
        self.assertIn("attestation_hash", cert)

    def test_strata_119_element_distribution_audit(self):
        temp_strata_db = Path(tempfile.gettempdir()) / "test_strata_119.db"
        if temp_strata_db.exists():
            temp_strata_db.unlink()

        conn = sqlite3.connect(temp_strata_db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE strata_nodes (
                node_id TEXT PRIMARY KEY,
                structural_zone TEXT NOT NULL,
                payload TEXT
            );
        """)

        elem_idx = 0
        for zone_name, info in CANONICAL_ZONES.items():
            for _ in range(info["count"]):
                node_id = f"ELEM_{elem_idx:03d}"
                cursor.execute(
                    "INSERT INTO strata_nodes (node_id, structural_zone, payload) VALUES (?, ?, ?);",
                    (node_id, zone_name, '{"status": "PERMINERALIZED"}')
                )
                elem_idx += 1
        conn.commit()
        conn.close()

        verifier = AshLedgerVerifier()
        verifier.load_sqlite(temp_strata_db, table_name="strata_nodes")
        strata_report = verifier.verify_strata()

        self.assertEqual(strata_report["status"], "VERIFIED")
        self.assertEqual(strata_report["unique_elements_count"], 119)
        
        # Dual-schema fallback for key compatibility
        consecrated_flag = strata_report.get("is_119_consecrated_distribution")
        if consecrated_flag is None:
            consecrated_flag = strata_report.get("is_119_consecrated_total")
        self.assertTrue(consecrated_flag)

if __name__ == "__main__":
    unittest.main()
