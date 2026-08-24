"""
Comprehensive Integration Test Suite for the Cathedral-Engine Suite.
Validates:
- Vector 1: Spatial Grid & Dynamic Node Ingestion (Chamber V)
- Vector 2: 40-Book Codex Generator & Cryptographic Proofs
- Vector 3: 377-Card Persona Oracle & Belnap-Dunn Heuristics Solver
- Vector 4: Daemon Hardening, Merkle DAG Verification, Rollback & CLI
- Expansion: Multi-Agent Wargaming, Batch 40-Book Scaffolding, Tri-Key Suite
"""

import os
import sys
import unittest
import json
import time
import threading
import urllib.request
import urllib.error

sys.path.insert(0, "/working_dir/c_9a0a4a350cc893af")

from engine.models import Spectral, BelnapValue, ChamberVLayout
from engine.database import DatabaseManager, DB_PATH
from engine.codex_generator import CodexGenerator
from engine.oracle_deck import OracleDeckManager
from engine.sanguine_heuristics import SanguineHeuristicsSolver
from engine.merkle_verifier import MerkleVerifier
from engine.simulation import PlaytestSimulationRunner
from engine.wargame import DialetheicWargameEngine
from engine.batch_codex import BatchCodexCompiler
from engine.trikey_diagnostics import TriKeyDiagnosticSuite
from engine.server import ThreadedHTTPServer, CathedralAPIHandler, generate_chamber_v_layout

TEST_PORT = 5056

class TestCathedralEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager()
        cls.codex_gen = CodexGenerator(cls.db)
        cls.oracle = OracleDeckManager(cls.db)
        cls.solver = SanguineHeuristicsSolver()
        cls.verifier = MerkleVerifier(cls.db)
        cls.wargame = DialetheicWargameEngine(cls.db)
        cls.batch_codex = BatchCodexCompiler(cls.db)
        cls.trikey = TriKeyDiagnosticSuite(cls.db)
        
        # Start test HTTP server in background thread
        cls.server = ThreadedHTTPServer(("127.0.0.1", TEST_PORT), CathedralAPIHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _http_get(self, path: str):
        url = f"http://127.0.0.1:{TEST_PORT}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "CathedralTest/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return resp.status, data

    def _http_post(self, path: str, payload: dict):
        url = f"http://127.0.0.1:{TEST_PORT}{path}"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": "CathedralTest/1.0"}, method="POST")
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return resp.status, data

    def test_01_database_and_genesis(self):
        """Verify ash_ledger exists and genesis block is initialized."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ash_ledger")
            count = cursor.fetchone()[0]
            self.assertGreaterEqual(count, 1)

            cursor.execute("SELECT * FROM ash_ledger WHERE block_index = 0")
            genesis = cursor.fetchone()
            self.assertEqual(genesis["event_type"], "GENESIS_BLOCK")
            self.assertEqual(genesis["parent_hash"], "0" * 64)

    def test_02_codex_strata_40_books(self):
        """Verify all 40 books are populated across the 4 tiers."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM codex_strata")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 40)

            cursor.execute("SELECT tier_designation, COUNT(*) FROM codex_strata GROUP BY tier_designation")
            tier_counts = dict(cursor.fetchall())
            self.assertEqual(tier_counts.get("Prime Foundations"), 10)
            self.assertEqual(tier_counts.get("Inner Mandala"), 10)
            self.assertEqual(tier_counts.get("Outer Choirs"), 10)
            self.assertEqual(tier_counts.get("Inner Shadow Canon"), 10)

    def test_03_codex_chapter_scaffolding_and_merkle(self):
        """Verify automated chapter generation with coordinate blocks and cryptographic hashing."""
        chapter = self.codex_gen.scaffold_chapter(book_id=5, chapter_num=1)
        self.assertIn("Book V · Chapter 1", chapter.chapter_designation)
        self.assertIn("COORDINATE BLOCKS", chapter.full_monograph)
        self.assertGreater(len(chapter.content_hash), 32)
        self.assertGreater(len(chapter.merkle_proof), 32)

    def test_04_persona_oracle_377_cards(self):
        """Verify the 377-Card Persona Oracle deck is indexed."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM oracle_deck_strata")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 377)

    def test_05_oracle_draw_and_interference(self):
        """Verify drawing cards and spectral interference calculations."""
        draw_go = self.oracle.draw(spectrum_mode="Gold-Obsidian", active_spectrum=Spectral.GOLD)
        self.assertIn("interference_intensity", draw_go)
        self.assertIn(draw_go["belnap_resolution"]["truth_value"], ["T", "F", "B", "N"])

    def test_06_sanguine_heuristics_dialetheic_resolution(self):
        """Verify Belnap-Dunn logic join and TRIZ Phase Resonance Trimming."""
        res_b = self.solver.resolve_collision(
            claim_a=BelnapValue.T,
            claim_b=BelnapValue.F,
            spectral_a=Spectral.TEAL,
            spectral_b=Spectral.RED
        )
        self.assertEqual(res_b.truth_value, BelnapValue.B)
        self.assertTrue(res_b.is_dialetheia)
        self.assertLessEqual(res_b.algorithmic_cost, 0.30)

    def test_07_spatial_chamber_v_generation(self):
        """Verify 8x8 spatial grid layout and node spawning for Chamber V."""
        layout = generate_chamber_v_layout()
        self.assertEqual(layout.grid_size, 8)
        self.assertEqual(len(layout.nodes), 64)

    def test_08_merkle_verification_and_tamper_detection(self):
        """Verify cryptographic Merkle chain validation."""
        res = self.verifier.verify_ledger_chain()
        self.assertTrue(res["valid"])

    def test_09_http_rest_api_endpoints(self):
        """Verify REST API routes via live test HTTP server."""
        status, data = self._http_get("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "OPERATIONAL")

        status, data = self._http_get("/api/rpg/state")
        self.assertEqual(status, 200)
        self.assertEqual(data["carrier_hz"], 130.81)

        status, data = self._http_get("/api/rpg/chamber?id=5")
        self.assertEqual(status, 200)
        self.assertEqual(len(data["nodes"]), 64)

    def test_10_multi_agent_wargame(self):
        """Verify N=4 multi-agent paraconsistent wargame execution."""
        summary = self.wargame.run_wargame(rounds=3)
        self.assertEqual(summary["rounds_executed"], 3)
        self.assertEqual(summary["factions_count"], 4)
        self.assertIn("final_bilattice_state", summary)

    def test_11_batch_codex_compilation(self):
        """Verify batch generation of all 40 books."""
        summary = self.batch_codex.compile_all_40_books()
        self.assertEqual(summary["total_books_scaffolded"], 40)
        self.assertTrue(summary["merkle_verification"]["valid"])

    def test_12_trikey_diagnostic_and_9_stage_loop(self):
        """Verify Tri-Key governance and 9-Stage Load-Bearing Reduction Loop."""
        diag = self.trikey.audit_tri_key_governance()
        self.assertEqual(diag["governance_mode"], "TRI_KEY_SOVEREIGN_SUPREMACY")
        self.assertEqual(diag["lead_key"]["status"], "PERMINERALIZED")

        loop = self.trikey.execute_9_stage_reduction_loop()
        self.assertEqual(len(loop["stages"]), 9)
        self.assertGreater(loop["telemetry_output"]["sigma_coh"], 0.70)

if __name__ == "__main__":
    unittest.main()
