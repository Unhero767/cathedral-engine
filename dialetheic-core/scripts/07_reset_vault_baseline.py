import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path: sys.path.insert(0, PARENT_DIR)

from src.archive_store import ArchiveStore

store = ArchiveStore()
store.save_state(afield_temp=300.0, flux=0.0)
store.set_meta("total_system_rpm", "77.45")
print("=== VAULT BASELINE RESET ===")
print("A-Field Temp reset to 300.0K, Flux reset to 0.00, System Speed reset to 77.45 RPM.")
