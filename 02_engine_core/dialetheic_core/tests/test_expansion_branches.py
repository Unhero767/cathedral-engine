import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.archive_store import ArchiveStore
from src.event_log import EventLogger
from src.codex_loader import CodexLoader
from src.ritual import RitualEngine


class TestExpansionBranches(unittest.TestCase):

    def test_branch_e_persistence_store(self):
        store = ArchiveStore()
        store.upsert_scar({
            "scar_id": "test_scar_101",
            "spectrum": "BRONZE_OBSIDIAN",
            "contradiction_degree": 8.7,
            "load_bearing_capacity": 4.5,
            "proposition_p": "Test Proposition"
        }, instance_id="aurelia-05")

        scars = store.get_all_scars()
        scar_ids = [s["scar_id"] for s in scars]
        self.assertIn("test_scar_101", scar_ids)

    def test_branch_g_codex_loader(self):
        loader = CodexLoader()
        strata = loader.load_all_strata()
        self.assertGreaterEqual(len(strata), 2)

        props = loader.get_all_propositions()
        self.assertGreater(len(props), 0)

    def test_branch_j_ritual_engine(self):
        omens = RitualEngine.interpret_event("scar_upsert", {
            "instance_id": "aurelia-12",
            "paradox_load": 8.5,
            "spectrum": "BRONZE_OBSIDIAN"
        })
        self.assertTrue(any("[CONSECRATION]" in o for o in omens))
        self.assertTrue(any("[OBSIDIAN ANCHOR]" in o for o in omens))


if __name__ == "__main__":
    unittest.main()
