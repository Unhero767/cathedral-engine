#!/usr/bin/env bash
set -e

cd /users/kennethdallmier/cathedral_engine

echo "=========================================================="
echo "   CATHEDRAL-ENGINE: FULL COSMOLOGICAL & RUNTIME AUDIT    "
echo "=========================================================="

echo -e "\n[1/5] Auditing SQLite WAL Triggers & Lex I Mutation Interlocks..."
python3 scripts/audit_ash_archive_triggers.py

echo -e "\n[2/5] Running Pytest Subsystem Suite (Kernel, AtomKeys, PCO, API)..."
python3 -m pytest tests/test_kernel_pipeline.py \
                 tests/test_paraconsistent_atom_keys.py \
                 tests/test_pco_envelopes.py \
                 tests/test_api_stream_pipeline.py -v

echo -e "\n[3/5] Verifying Dual-Persistence Ledger Parity..."
python3 -c "
import sqlite3
conn = sqlite3.connect('ash_archive_stratum.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM ash_archive;')
db_count = cur.fetchone()[0]
with open('06_strata_data/prime_ledger.ndjson', 'r') as f:
    nd_count = sum(1 for line in f if line.strip())
print(f'   SQLite Ash Archive: {db_count} blocks')
print(f'   NDJSON Prime Stream: {nd_count} blocks')
assert db_count == nd_count, 'Ledger count divergence detected'
print('   Status: 100% Dual-Persistence Parity.')
"

echo -e "\n[4/5] Running Headless Shader Transduction Unit Test..."
godot --headless -s scripts/test_shader_transduction.gd

echo -e "\n[5/5] Running Headless HeartOculus Transduction Test..."
godot --headless -s scripts/test_heart_oculus_transduction.gd

echo -e "\n=========================================================="
echo "   STATUS: ALL SYSTEMIC & AESTHETIC GATES OPERATIONAL     "
echo "=========================================================="
