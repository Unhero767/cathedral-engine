#!/usr/bin/env bash
set -e

cd /users/kennethdallmier/cathedral_engine

echo "Starting Godot Headless Listener..."
godot --headless -s scripts/test_presentation_runner.gd &
GODOT_PID=$!

echo "Waiting for Godot WebSocket handshake to establish (2s)..."
sleep 2

echo "Firing Contradictory Batch Ingress payload..."
curl -s -X POST http://127.0.0.1:8765/v1/events/ingest/batch \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "event_id": "GD-005",
        "atom_key": "Spire.Resonance",
        "lamport_clock": 60,
        "source_timestamp": '$(date +%s)',
        "actor": "Arbiter-Alpha",
        "polarity": true,
        "value": {"strain": 0.44},
        "parents": [],
        "register": "E"
      },
      {
        "event_id": "GD-006",
        "atom_key": "Spire.Resonance",
        "lamport_clock": 61,
        "source_timestamp": '$(date +%s)',
        "actor": "Arbiter-Beta",
        "polarity": false,
        "value": {"strain": 0.91},
        "parents": ["GD-005"],
        "register": "E"
      }
    ]
  }' > /dev/null

echo "Ingress dispatched. Waiting for Godot test runner completion..."
wait $GODOT_PID
echo "Live Presentation Test: SUCCESS (Exit 0)."
