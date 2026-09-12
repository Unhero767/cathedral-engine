"""
Asset 8: Ash Archive Vault Snapshot Exporter.
Exports SQLite harmonic_scars and archive_state to a JSON snapshot file.
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path: sys.path.insert(0, PARENT_DIR)

from src.archive_store import ArchiveStore

def export_snapshot():
    store = ArchiveStore()
    state = store.get_state()
    scars = store.get_all_scars()

    snapshot = {
        "snapshot_id": "ash-archive-export-v1",
        "afield": state,
        "scars_count": len(scars),
        "harmonic_scars": scars
    }

    out_path = Path("data/ash_archive_snapshot.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot successfully exported to {out_path.resolve()} ({len(scars)} scars saved).")

if __name__ == "__main__":
    export_snapshot()
