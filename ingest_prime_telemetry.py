#!/usr/bin/env python3
"""
Ingest prime_ledger.ndjson simulation frames into SQLite telemetry & experiment tables.
Dallmier Tech Venture (Olney, Illinois)
"""

import hashlib, json, sqlite3
from pathlib import Path

db_path = Path("./ash_archive.db").resolve()
ndjson_path = Path("./06_strata_data/prime_ledger.ndjson").resolve()

if not ndjson_path.exists():
    print(f"Error: {ndjson_path} does not exist.")
    exit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

ingested_telemetry = 0
ingested_experiments = 0

with open(ndjson_path, "r", encoding="utf-8") as f:
    for line in f:
        clean = line.strip()
        if not clean:
            continue
        data = json.loads(clean)
        
        # Canonical hash of the simulation frame payload
        frame_payload = json.dumps(data, sort_keys=True, separators=(",", ":"))
        merkle_hash = hashlib.sha256(frame_payload.encode("utf-8")).hexdigest()
        
        ts = data.get("timestamp")
        spectrum = data.get("spectrum", "Bronze-Obsidian/Null")
        phi = float(data.get("phi", 0.0))
        metrics = data.get("metrics", {})
        truth_state = metrics.get("truth_state", "Both")
        raw_payload = data.get("payload", "")
        
        # 1. Inscribe to telemetry_stream
        cur.execute(
            "INSERT INTO telemetry_stream (timestamp, tier, payload) VALUES (?, ?, ?);",
            (ts, "SIMULATION_FRAME", frame_payload)
        )
        ingested_telemetry += 1
        
        # 2. Inscribe to lab_experiments
        cur.execute(
            """INSERT INTO lab_experiments 
               (timestamp, experiment_name, spectral_constant, belnap_state, phi_rate, merkle_hash, payload) 
               VALUES (?, ?, ?, ?, ?, ?, ?);""",
            (ts, "EAS-03_SHADOW_CANON_COLLISION", spectrum, truth_state, phi, merkle_hash, raw_payload)
        )
        ingested_experiments += 1

conn.commit()
conn.close()

print(f"Ingestion complete: {ingested_telemetry} frames inscribed to telemetry_stream and lab_experiments.")
