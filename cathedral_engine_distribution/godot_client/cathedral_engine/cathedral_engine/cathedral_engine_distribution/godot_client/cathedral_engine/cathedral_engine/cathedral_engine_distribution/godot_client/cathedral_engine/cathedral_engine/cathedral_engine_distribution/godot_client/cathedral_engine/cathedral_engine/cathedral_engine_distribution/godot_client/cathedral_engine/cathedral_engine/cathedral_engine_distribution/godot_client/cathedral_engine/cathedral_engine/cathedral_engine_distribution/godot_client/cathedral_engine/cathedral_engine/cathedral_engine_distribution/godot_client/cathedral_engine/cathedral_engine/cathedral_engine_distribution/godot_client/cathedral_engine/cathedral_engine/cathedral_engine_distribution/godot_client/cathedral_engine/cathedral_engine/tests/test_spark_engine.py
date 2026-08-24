import unittest
import tempfile
import shutil
import os
import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent.parent
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from mlaos_park.spark_orchestrator import MLAOSparkOrchestrator
from mlaos_park.models import AuthorityLevel, TaskLifecycleState

class TestMLAOSparkEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.spark = MLAOSparkOrchestrator(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_seven_layer_execution_cycle(self):
        res = self.spark.execute_seven_layer_cycle(
            task_title="Test Carrier Alignment",
            protocol_id="PROTO_CARRIER_CALIBRATE",
            parameters={"target_hz": 43.7}
        )
        self.assertTrue(res["success"])
        self.assertTrue(res["merkle_chain_root"].startswith("0x"))
        self.assertGreater(res["phi_coherence"], 0.8)

    def test_abyss_buffer_contradiction_capture(self):
        scar = self.spark.abyss.record_contradiction(
            claim_a="Statement P",
            evidence_a="Sensor 1",
            claim_not_a="Statement ¬P",
            evidence_not_a="Sensor 2",
            context="Dialetheic Test"
        )
        self.assertTrue(scar["scar_id"].startswith("SCAR_"))
        self.assertEqual(scar["lattice_value"], "Both (T ∧ F)")

    def test_spark_0_pilot_run(self):
        pilot = self.spark.run_spark_0_pilot()
        self.assertEqual(pilot["pilot"], "SPARK-0")
        self.assertEqual(pilot["status"], "RATIFIED & OPERATIONAL")

if __name__ == "__main__":
    unittest.main()
