import unittest
import os
import sys
import tempfile
import json
import shutil
from pathlib import Path

# Add cathedral_engine to path
ENGINE_ROOT = Path(__file__).resolve().parent.parent
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from engines.paraconsistent_engine import EAS03ParaconsistentEngine, BelnapDunnTruthState
from engines.emotional_physics_engine import EmotionalPhysicsEngine
from engines.arcana_engine import ArcanaEngine
from engines.codex_engine import CodexManager
from engines.ledger_engine import LedgerEngine, ConstitutionViolation
from engines.campaign_engine import CampaignEngine

class TestParaconsistentEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.ledger_path = os.path.join(self.temp_dir, "test_ledger.ndjson")
        self.engine = EAS03ParaconsistentEngine(ledger_path=self.ledger_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_belnap_dunn_states(self):
        self.assertEqual(self.engine.compute_belnap_dunn_state(0.8, 0.8), BelnapDunnTruthState.BOTH)
        self.assertEqual(self.engine.compute_belnap_dunn_state(0.8, 0.2), BelnapDunnTruthState.TRUE)
        self.assertEqual(self.engine.compute_belnap_dunn_state(0.2, 0.8), BelnapDunnTruthState.FALSE)
        self.assertEqual(self.engine.compute_belnap_dunn_state(0.2, 0.2), BelnapDunnTruthState.NONE)

    def test_frame_tick_and_merkle(self):
        res = self.engine.process_frame_tick(1, c_pos=0.9, c_neg=0.9)
        self.assertEqual(res["state"], BelnapDunnTruthState.BOTH)
        self.assertEqual(self.engine.crystallized_scars, 1)
        self.assertTrue(res["merkle_tip"].startswith("0x"))
        self.assertTrue(os.path.exists(self.ledger_path))

class TestEmotionalPhysicsEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EmotionalPhysicsEngine(target_baseline=0.78200)

    def test_kinetic_state_integral(self):
        theta_e, err = self.engine.calculate_kinetic_state(0.95, 0.81)
        expected = 0.95 * 0.81  # Integral of C * e^(-t) from 0 to inf is C
        self.assertAlmostEqual(theta_e, expected, places=3)

    def test_harmonization_and_awareness(self):
        m_d = 0.95
        l_p = 0.81
        hc = self.engine.calculate_harmonization_constant(m_d, l_p)
        self.assertAlmostEqual(hc, 0.78200 - (m_d * l_p), places=4)
        omega = self.engine.calculate_awareness_index(hc, m_d)
        self.assertGreater(omega, 0.0)

    def test_anticipatory_buffer(self):
        state = {
            "emotional_physics_constants": {
                "memory_delta": 0.95,
                "luminous_probability": 0.75,
                "harmonization_constant": 0.01
            }
        }
        res = self.engine.apply_anticipatory_buffer(state)
        self.assertTrue(res["buffer_applied"])
        self.assertEqual(res["emotional_physics_constants"]["luminous_probability"], 0.77)
        self.assertEqual(res["emotional_physics_constants"]["harmonization_constant"], 0.06)

class TestArcanaEngine(unittest.TestCase):
    def setUp(self):
        self.arcana = ArcanaEngine()

    def test_deck_structure(self):
        # 7 Flux Majors + (7 Chromas * 7 Identity Vectors = 49) + 22 Rebellion = 78 cards
        self.assertEqual(len(self.arcana.deck), 78)

    def test_action_resolution(self):
        res = self.arcana.resolve_action("Test Surge", stat_bonus=2)
        self.assertIn("outcome", res)
        self.assertIn("drawn_card", res)
        self.assertIn(res["dice"][0], range(1, 7))
        self.assertIn(res["dice"][1], range(1, 7))

    def test_monte_carlo(self):
        mc = self.arcana.simulate_vector_interference(100)
        self.assertEqual(mc["iterations"], 100)
        total_pct = sum(mc["percentages"].values())
        self.assertAlmostEqual(total_pct, 100.0, places=0)

class TestCodexManager(unittest.TestCase):
    def setUp(self):
        self.mgr = CodexManager(str(ENGINE_ROOT))

    def test_strata_mapping(self):
        self.assertEqual(self.mgr.get_stratum_for_book(1), "Prime Foundations")
        self.assertEqual(self.mgr.get_stratum_for_book(15), "Inner Mandala")
        self.assertEqual(self.mgr.get_stratum_for_book(25), "Outer Choirs")
        self.assertEqual(self.mgr.get_stratum_for_book(35), "Shadow Canon")

    def test_monograph_format(self):
        mono = self.mgr.format_canonical_monograph("I", "The Threshold", "Gold/Joy", "Payload text")
        self.assertIn("## Section I: Opening Movement & Spectral Dominant", mono)
        self.assertIn("## Section II: Foundational Strata & Structural Anchors", mono)
        self.assertIn("## Section III: Dialetheic Buffer & Paraconsistent Collision", mono)
        self.assertIn("## Section IV: Synthesis & Harmonic Scar Integration", mono)

    def test_list_books(self):
        books = self.mgr.list_books()
        self.assertGreaterEqual(len(books), 40)

class TestLedgerEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_ledger.db")
        self.ledger = LedgerEngine(db_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_entity_creation_and_overwrite_block(self):
        self.ledger.create_entity(
            entity_id="CORE-001",
            name="Axiomatic Threshold",
            definition="First structural boundary",
            entity_type="Axiom",
            author="Kenneth Dallmier",
            reason="Genesis inscription"
        )
        with self.assertRaises(ConstitutionViolation):
            self.ledger.create_entity(
                entity_id="CORE-001",
                name="Duplicate",
                definition="Collision attempt",
                entity_type="Axiom",
                author="Unknown",
                reason="Invalid overwrite"
            )

    def test_contradiction_quarantine(self):
        self.ledger.create_entity(
            entity_id="CORE-002",
            name="Dialetheic Node",
            definition="Node capable of contradictory claims",
            entity_type="Node",
            author="Kenneth Dallmier",
            reason="Genesis initialization"
        )
        self.ledger.add_claim("CORE-002", "Consciousness is lithic.", "Architect", "Initial affirmative claim")
        self.ledger.add_claim("CORE-002", "!Consciousness is lithic.", "Architect", "Paraconsistent negation claim")
        
        contras = self.ledger.get_contradictions("CORE-002")
        self.assertEqual(len(contras), 1)
        self.assertEqual(contras[0]["status"], "QUARANTINED")

class TestCampaignEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_campaign.db")
        self.camp = CampaignEngine(db_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_party_and_strain(self):
        party = self.camp.get_party()
        self.assertGreaterEqual(len(party), 2)
        kiri = next(p for p in party if p["name"] == "Kiri Vespera")
        strain = self.camp.calculate_total_strain(kiri["id"])
        self.assertGreater(strain, 0.0)

    def test_combat_turn(self):
        res = self.camp.record_combat_turn("Kiri Vespera", "Void Slash", stat_mod=2)
        self.assertIn("outcome", res)
        self.assertTrue(res["ledger_hash"].startswith("0x"))

if __name__ == "__main__":
    unittest.main()
