import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sovereign_protocol_executor import SovereignProtocolExecutor
from src.tri_key_authority import TriKeyAuthority
from src.asema_anomaly_containment import AsemaAnomalyContainment
from src.rpg_bridge import RPGDialetheicBridge
from src.cathedral_engine import CathedralEngineSimulation

class TestSovereignSuite(unittest.TestCase):

    def test_asset3_decalogue_compliance(self):
        res = SovereignProtocolExecutor.audit_decalogue_compliance({"afield": {"temp": 305.0}})
        self.assertEqual(res["status"], "COMPLIANT")

    def test_asset4_tri_key_authority(self):
        token = TriKeyAuthority.generate_token("LEAD_KEY")
        self.assertTrue(TriKeyAuthority.verify_key_signature("LEAD_KEY", token))

    def test_asset5_asema_containment(self):
        mgr = AsemaAnomalyContainment()
        res = mgr.evaluate_k_index("ASEMA-01", k_index=4.2, proposition="Test Anomaly")
        self.assertEqual(res["action"], "ASEMA_QUARANTINE_SEALED")

    def test_rpg_bridge_event(self):
        sim = CathedralEngineSimulation()
        bridge = RPGDialetheicBridge(simulation=sim)
        res = bridge.process_tile_event("Aurelia", "A_FIELD_THERMAL", paradox_charge=8.2, heat_delta=25.0)
        self.assertIn("scar_forged", res)


if __name__ == "__main__":
    unittest.main()
