import unittest
import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_server import app


class TestAPIServer(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "stable")

    def test_state_endpoint(self):
        response = self.client.get("/state")
        self.assertEqual(response.status_code, 200)
        self.assertIn("afield", response.json())
        self.assertIn("scars", response.json())

    def test_node_sync_route_aliases(self):
        payload = {
            "instance_id": "aurelia-12",
            "mqi_score": 88.5,
            "a_field_temperature_k": 305.0,
            "current_flux": 2.4,
            "active_spectrum": "GOLD",
            "active_paradox_load": 8.42
        }

        # Test top-level /node/sync route
        resp1 = self.client.post("/node/sync", json=payload)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp1.json()["instance_id"], "aurelia-12")

        # Test /sync route alias
        resp2 = self.client.post("/sync", json=payload)
        self.assertEqual(resp2.status_code, 200)

        # Test /api/v1/node/sync
        resp3 = self.client.post("/api/v1/node/sync", json=payload)
        self.assertEqual(resp3.status_code, 200)

    def test_invalid_input_rejection(self):
        payload = {
            "instance_id": "invalid-node",  # Fails regex pattern ^aurelia-(0[1-9]|[1-4][0-9])$
            "mqi_score": 50.0,
            "a_field_temperature_k": 300.0,
            "current_flux": 1.0,
            "active_spectrum": "TEAL",
            "active_paradox_load": 5.0
        }
        resp = self.client.post("/node/sync", json=payload)
        self.assertEqual(resp.status_code, 422)


if __name__ == "__main__":
    unittest.main()
