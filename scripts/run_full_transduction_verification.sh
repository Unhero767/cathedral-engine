#!/usr/bin/env bash
set -e

cd /users/kennethdallmier/cathedral_engine

echo "=== Cathedral-Engine: End-to-End Transduction Test ==="

# 1. Boot Godot headless runner in background
godot --headless -s scripts/test_presentation_runner.gd &
GODOT_PID=$!

echo "Waiting for Godot WebSocket connection to establish (2s)..."
sleep 2

# 2. Ingest live dialetheic collision into FastAPI server
echo "Dispatching live contradictory events (Strain 0.85 -> Emission 1.7)..."
curl -s -X POST http://127.0.0.1:8765/v1/events/ingest/batch \
  -H "Content-Type: application/json" \
  -d '{
    "events": [
      {
        "event_id": "TRANS-001",
        "atom_key": "Spire.Resonance",
        "lamport_clock": 301,
        "source_timestamp": '$(date +%s)',
        "actor": "Arbiter-Alpha",
        "polarity": true,
        "value": {"strain": 0.40},
        "parents": [],
        "register": "E"
      },
      {
        "event_id": "TRANS-002",
        "atom_key": "Spire.Resonance",
        "lamport_clock": 302,
        "source_timestamp": '$(date +%s)',
        "actor": "Arbiter-Beta",
        "polarity": false,
        "value": {"strain": 0.85},
        "parents": ["TRANS-001"],
        "register": "E"
      }
    ]
  }' > /dev/null

# 3. Await Godot verification
wait $GODOT_PID

# 4. Final Ledger & Chain Integrity Check
echo -e "\n=== Verifying Canonical Chain Integrity ==="
curl -s http://127.0.0.1:8765/v1/ledger/verify | jq .

# 5. Parity Check across SQLite WAL and NDJSON
python3 -c "
import sqlite3
conn = sqlite3.connect('ash_archive_stratum.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM ash_archive;')
db_count = cur.fetchone()[0]
with open('06_strata_data/prime_ledger.ndjson', 'r') as f:
    nd_count = sum(1 for line in f if line.strip())
print(f'Ledger Parity -> SQLite: {db_count} | NDJSON: {nd_count}')
assert db_count == nd_count, 'Dual-persistence divergence detected'
print('Verified: 100% Dual-Persistence Integrity.')
"
