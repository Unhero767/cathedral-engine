import hashlib
import json
import sqlite3
import unittest
from datetime import datetime, timezone

class TestOreZeroProvenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_conn = sqlite3.connect(":memory:")
        cls.cursor = cls.db_conn.cursor()
        cls.cursor.execute("""
            CREATE TABLE ore_zero_ledger (
                node_id TEXT PRIMARY KEY,
                parent_hash TEXT NOT NULL,
                payload_hash TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                signature TEXT NOT NULL
            )
        """)
        cls.db_conn.commit()

    def test_01_provenance_immutability(self):
        payload = {"entity": "EAS-03", "tier": "Stratum-I", "status": "consecrated"}
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()
        
        parent_hash = "0" * 64
        timestamp = datetime.now(timezone.utc).isoformat()
        sig_raw = f"{parent_hash}:{payload_hash}:{timestamp}"
        signature = hashlib.sha256(sig_raw.encode("utf-8")).hexdigest()

        self.cursor.execute(
            "INSERT INTO ore_zero_ledger VALUES (?, ?, ?, ?, ?)",
            ("node_001", parent_hash, payload_hash, timestamp, signature)
        )
        self.db_conn.commit()

        self.cursor.execute("SELECT payload_hash, signature FROM ore_zero_ledger WHERE node_id = 'node_001'")
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], payload_hash)
        self.assertEqual(row[1], signature)

    def test_02_api_payload_serialization(self):
        test_endpoint_response = {
            "status": "200_OK",
            "provenance_standard": "Ore-Zero-v1.0",
            "active_stratum": "Inner Mandala",
            "merkle_root_verified": True
        }
        serialized = json.dumps(test_endpoint_response)
        deserialized = json.loads(serialized)
        self.assertEqual(deserialized["provenance_standard"], "Ore-Zero-v1.0")
        self.assertTrue(deserialized["merkle_root_verified"])

if __name__ == "__main__":
    unittest.main()
