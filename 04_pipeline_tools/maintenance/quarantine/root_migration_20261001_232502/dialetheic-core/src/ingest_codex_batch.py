"""
Batch Codex Ingestion Script - Ingests all JSON files in codex/ directory
and processes propositions through VectorMapper, DialetheicBuffer, and ArchiveStore.
"""

import os
import sys
import json
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from src.codex_loader import CodexLoader
from src.cathedral_engine import CathedralEngineSimulation
from src.vector_mapper import AshArchiveMapper
from src.archive_store import ArchiveStore

def run_batch_ingestion():
    archive_store = ArchiveStore()
    sim = CathedralEngineSimulation(store=archive_store)
    mapper = AshArchiveMapper(buffer=sim.buffer)
    loader = CodexLoader()

    props = loader.get_all_propositions()
    print(f"Loaded {len(props)} propositions from codex/ directory.")

    ingested_count = 0
    for p in props:
        claim = p.get("claim") or p.get("text", "")
        counter_claim = p.get("counter_claim") or "Unmanifested opposition."
        prop_id = p.get("id", f"PROP-{ingested_count+1}")

        if claim and counter_claim:
            rec = mapper.ingest_verse_pair(claim, counter_claim, prop_id)
            eval_res = rec["evaluation"]
            
            if "scar" in eval_res:
                archive_store.upsert_scar({
                    "scar_id": prop_id,
                    "instance_id": f"STRATUM-{p.get('stratum', 1)}",
                    "spectrum": rec["spectrum"],
                    "paradox_load": rec["paradox_load"],
                    "capacity": rec["evaluation"]["scar"].load_bearing_capacity,
                    "proposition_p": f"[{prop_id}] {claim}"
                })
                ingested_count += 1

    sim.save_to_vault()
    print(f"Batch Ingestion Complete: {ingested_count} scars sealed in Archive Vault.")
    print(f"Total Active Scars in Buffer: {len(sim.buffer.harmonic_scars)}")
    print(f"A-Field Temperature: {sim.a_field_temp:.1f}K | System Speed: {sim.total_system_rpm:.2f} RPM")

if __name__ == "__main__":
    run_batch_ingestion()
