#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Lithic Healing Merkle DAG Ingestion Script
# File: ingest_healing_dag.py
# ==============================================================================

import json
import hashlib
import os
from datetime import datetime

HEALING_SOURCE = "strata/lithic_healing_ledger.json"
LEDGER_DEST = "strata/ash_archive_ledger.jsonl"

def compute_hash(payload: dict, prev_hash: str) -> str:
    serialized = json.dumps(payload, sort_keys=True) + prev_hash
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def ingest_healing_ledger():
    print("[CATHE_DAG] Initiating Lithic Healing Merkle DAG anchoring protocol...")
    
    if not os.path.exists(HEALING_SOURCE):
        print(f"[CATHE_ERR] Healing telemetry source not found at {HEALING_SOURCE}. Run simulate_polymer_healing.py first.")
        return

    os.makedirs(os.path.dirname(LEDGER_DEST), exist_ok=True)
    
    with open(HEALING_SOURCE, 'r') as f:
        records = json.load(f)

    # Fetch the last hash from the existing ledger to maintain continuity
    prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    if os.path.exists(LEDGER_DEST):
        with open(LEDGER_DEST, 'r') as ledger_file:
            lines = ledger_file.readlines()
            if lines:
                last_record = json.loads(lines[-1].strip())
                prev_hash = last_record.get("block_hash", prev_hash)

    ingested_count = 0
    with open(LEDGER_DEST, 'a') as ledger_file:
        for record in records:
            block_data = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "stratum_type": "LITHIC_AUTONOMOUS_HEALING",
                "remediation_telemetry": record
            }
            block_hash = compute_hash(block_data, prev_hash)
            
            node_entry = {
                "prev_hash": prev_hash,
                "block_hash": block_hash,
                "data": block_data
            }
            
            ledger_file.write(json.dumps(node_entry) + "\n")
            prev_hash = block_hash
            ingested_count += 1
            print(f"[CATHE_DAG] Anchored Healing Node Hash: {block_hash[:16]}... [Node {record['node_id']}: {record['remediation_status']}]")

    print(f"[CATHE_DAG] Successfully anchored {ingested_count} remediation records into {LEDGER_DEST}.")

if __name__ == "__main__":
    ingest_healing_ledger()
