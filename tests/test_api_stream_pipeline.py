"""
Cathedral-Engine: Phase II End-to-End Ingress & WebSocket Integration Test.
Runs in an isolated temporary stratum to preserve production ledger invariants.
"""
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.server import app

client = TestClient(app)

def test_api_batch_ingest_and_ws_stream():
    # 1. Subscribe to Read-Only WebSocket stream
    with client.websocket_connect("/ws/manifold") as ws:
        # Ingest out-of-order batch
        payload = {
            "events": [
                {
                    "event_id": "EVT-ISOLATED-002",
                    "atom_key": "Spire.Resonance",
                    "lamport_clock": 200,
                    "source_timestamp": 200.2,
                    "actor": "Observer-Beta",
                    "polarity": False,  # Contradicts Alpha -> B (Harmonic Scar)
                    "value": {"strain": 0.88},
                    "parents": ["EVT-ISOLATED-001"],
                    "register": "E"
                },
                {
                    "event_id": "EVT-ISOLATED-001",
                    "atom_key": "Spire.Resonance",
                    "lamport_clock": 199,
                    "source_timestamp": 200.1,
                    "actor": "Observer-Alpha",
                    "polarity": True,
                    "value": {"strain": 0.45},
                    "parents": [],
                    "register": "E"
                }
            ]
        }

        resp = client.post("/v1/events/ingest/batch", json=payload)
        assert resp.status_code == 200
        pcos = resp.json()
        assert len(pcos) == 2

        # Assert CausalSorter re-sequenced EVT-001 first (clock 199), then EVT-002 (clock 200)
        assert pcos[0]["provenance"]["tick"] == 199
        assert pcos[1]["provenance"]["tick"] == 200

        # Assert EVT-002 crystallized into Harmonic Scar (B)
        assert pcos[1]["epistemic_register"] == "S"
        assert pcos[1]["uncertainty_metadata"]["belnap_state"] == "B"
        assert pcos[1]["uncertainty_metadata"]["is_harmonic_scar"] is True

        # 2. Receive WebSocket Broadcast Frames
        frame1 = json.loads(ws.receive_text())
        assert frame1["provenance"]["tick"] == 199
        frame2 = json.loads(ws.receive_text())
        assert frame2["provenance"]["tick"] == 200

    # 3. Verify Ledger DAG endpoint reports valid chain
    verify_resp = client.get("/v1/ledger/verify")
    assert verify_resp.status_code == 200
    dag_status = verify_resp.json()
    assert dag_status["is_valid"] is True
