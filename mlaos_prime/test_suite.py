"""
test_suite.py - Verification Tests for MLAOS-Prime Core
"""
import unittest
import os
from axioms import BelnapDunnEngine, FourValuedLogic
from ledger import AshArchive
from paraconsistent import DialetheicReasoner

class TestMLAOSPrimeCore(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_ash_archive.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.ledger = AshArchive(db_path=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_belnap_dunn_operations(self):
        self.assertEqual(
            BelnapDunnEngine.conjunction_truth(FourValuedLogic.TRUE, FourValuedLogic.FALSE),
            FourValuedLogic.FALSE
        )
        self.assertEqual(
            BelnapDunnEngine.knowledge_join(FourValuedLogic.TRUE, FourValuedLogic.FALSE),
            FourValuedLogic.BOTH
        )
        self.assertTrue(BelnapDunnEngine.is_designated(FourValuedLogic.BOTH))

    def test_ledger_immutability_trigger(self):
        h1 = self.ledger.append({"test": "payload1"})
        self.assertTrue(self.ledger.verify_integrity())
        
        import sqlite3
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            with self.assertRaises(sqlite3.OperationalError):
                cursor.execute("UPDATE blocks SET payload = 'corrupted' WHERE index_id = 1")
            with self.assertRaises(sqlite3.OperationalError):
                cursor.execute("DELETE FROM blocks WHERE index_id = 1")

    def test_metamorphic_squeeze(self):
        reasoner = DialetheicReasoner(self.ledger)
        result = reasoner.evaluate_pair("System is operational", "System is offline", FourValuedLogic.TRUE, FourValuedLogic.TRUE)
        self.assertEqual(result["truth_value"], FourValuedLogic.BOTH.value)
        self.assertEqual(result["scar"]["crystallization_angle"], 54.74)

if __name__ == "__main__":
    unittest.main()
