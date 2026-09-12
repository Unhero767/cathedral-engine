import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path: sys.path.insert(0, PARENT_DIR)

from src.sovereign_protocol_executor import SovereignProtocolExecutor
from src.archive_store import ArchiveStore

store = ArchiveStore()
state = store.get_state()
audit = SovereignProtocolExecutor.audit_decalogue_compliance({"afield": state})

print("=== DECALOGUE COMPLIANCE AUDIT ===")
print("Status        :", audit["status"])
print("Lex I (Never-Overwrite):", audit["lex_1_never_overwrite"])
print("Lex X (Binary Covenant):", audit["lex_10_binary_covenant"])
print("Violations Count       :", audit["violations_count"])
