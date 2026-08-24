import unittest
import os
import sys
import sqlite3
import tempfile
import shutil
from pathlib import Path

# Add cathedral_engine to path
ENGINE_ROOT = Path(__file__).resolve().parent.parent
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from engines.enemy_engine import EnemyEngine, EnemySpectrum
from engines.dialogue_engine import DialogueEngine
from engines.progression_engine import ProgressionEngine
from engines.game_loop_engine import GameLoopEngine, GameState
from engines.chamber_generator import ChamberGeneratorEngine
from engines.save_manager import SaveManagerEngine
from engines.character_creation_engine import CharacterCreationEngine
from engines.universe_atlas_engine import UniverseAtlasEngine

class TestEnemyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = EnemyEngine()

    def test_archetypes_and_spawn(self):
        self.assertIn("LITHIC_SENTINEL", self.engine.archetypes)
        sentinel = self.engine.spawn_enemy("LITHIC_SENTINEL", "test_e1", 5, 2)
        self.assertEqual(sentinel.name, "Lithic Sentinel")
        self.assertEqual(sentinel.max_hp, 45)
        self.assertEqual(sentinel.armor, 4)
        self.assertEqual(sentinel.spectrum, EnemySpectrum.GOLD)

        shade = self.engine.spawn_enemy("VOID_SHADE", "test_e2", 5, 2)
        self.assertEqual(shade.spectrum, EnemySpectrum.OBSIDIAN)
        self.assertTrue(shade.can_phase_through_walls)

        synthete = self.engine.spawn_enemy("ROGUE_SYNTHETE", "test_e3", 5, 2)
        self.assertEqual(synthete.spectrum, EnemySpectrum.CRIMSON)
        self.assertEqual(synthete.max_ap, 5)

    def test_chromatic_matrix(self):
        # Gold is effective against Obsidian (1.5x)
        self.assertEqual(self.engine.calculate_chromatic_multiplier(EnemySpectrum.GOLD, EnemySpectrum.OBSIDIAN), 1.5)
        # Crimson is effective against Gold (1.5x)
        self.assertEqual(self.engine.calculate_chromatic_multiplier(EnemySpectrum.CRIMSON, EnemySpectrum.GOLD), 1.5)
        # Sapphire is resistant to Crimson (0.5x)
        self.assertEqual(self.engine.calculate_chromatic_multiplier(EnemySpectrum.CRIMSON, EnemySpectrum.SAPPHIRE), 0.5)

    def test_ai_decision_tree_and_distance_checks(self):
        enemy = self.engine.spawn_enemy("LITHIC_SENTINEL", "test_e1", 5, 2)
        actions = self.engine.decide_ai_turn(enemy, target_x=4, target_y=2, target_spectrum=EnemySpectrum.OBSIDIAN)
        self.assertGreaterEqual(len(actions), 1)
        self.assertTrue(any(a["type"] in ("ATTACK", "ABILITY", "MOVE") for a in actions))

    def test_paradox_threshold_reactions(self):
        shade = self.engine.spawn_enemy("VOID_SHADE", "test_e2", 5, 2)
        actions = self.engine.decide_ai_turn(shade, target_x=4, target_y=2, player_paradox=5)
        self.assertTrue(any(a.get("reaction") == "DIALETHEIC_SELF_DESTRUCT" for a in actions))

        synthete = self.engine.spawn_enemy("ROGUE_SYNTHETE", "test_e3", 5, 2)
        actions_syn = self.engine.decide_ai_turn(synthete, target_x=4, target_y=2, player_paradox=5)
        self.assertTrue(synthete.is_overdriven)

class TestDialogueEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_dialogue.db")
        self.engine = DialogueEngine(db_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_node_retrieval(self):
        node = self.engine.get_node("CHAMBER_I_LITHIC", "start")
        self.assertIsNotNone(node)
        self.assertEqual(node.speaker, "Aurelia-9")
        self.assertGreaterEqual(len(node.options), 2)

    def test_option_selection(self):
        res = self.engine.select_option("CHAMBER_I_LITHIC", "start", 0, stat_value=5)
        self.assertIn("skill_passed", res)
        self.assertIn("consequence", res)

    def test_quests(self):
        quests = self.engine.get_active_quests()
        self.assertGreaterEqual(len(quests), 5)

class TestProgressionEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_prog.db")
        self.engine = ProgressionEngine(db_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_character_stats(self):
        stats = self.engine.get_character_stats("Kiri Vespera")
        self.assertIsNotNone(stats)
        self.assertEqual(stats["level"], 1)
        self.assertGreaterEqual(stats["unspent_insight"], 50)

    def test_unlock_talent(self):
        res = self.engine.unlock_talent("Kiri Vespera", "T_VOID_SURGE", "Void Walker")
        self.assertTrue(res.get("success", False))
        updated = self.engine.get_character_stats("Kiri Vespera")
        self.assertEqual(updated["max_ap"], 5)

    def test_craft_relic(self):
        res = self.engine.craft_relic("RECIPE_HGASE_PRISM", owner_id=1)
        self.assertTrue(res.get("success", False))
        self.assertEqual(res["crafted_item"], "Refined HGASE Resonator Prism")

class TestGameLoopEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GameLoopEngine(base_dir=str(ENGINE_ROOT))

    def test_session_init(self):
        state = self.engine.start_new_game("Kiri Vespera", "Void Walker")
        self.assertEqual(state["game_state"], GameState.EXPLORATION.value)
        self.assertEqual(state["player"]["x"], 1)
        self.assertEqual(state["player"]["y"], 1)

    def test_movement(self):
        state = self.engine.player_move(2, 1)
        self.assertEqual(state["player"]["x"], 2)
        self.assertEqual(state["player"]["y"], 1)

    def test_combat_flow_and_chroma(self):
        self.engine.trigger_combat_encounter()
        self.assertEqual(self.engine.state, GameState.TACTICAL_COMBAT)
        self.assertGreaterEqual(len(self.engine.active_combat_squad), 1)

        target_uid = self.engine.active_combat_squad[0].uid
        state = self.engine.player_attack(target_uid, "Resonance Strike", attack_spectrum=EnemySpectrum.GOLD)
        self.assertLess(state["player"]["ap"], state["player"]["max_ap"])

        state_after_turn = self.engine.end_player_turn()
        self.assertEqual(state_after_turn["player"]["ap"], state_after_turn["player"]["max_ap"])

class TestChamberGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ChamberGeneratorEngine()

    def test_generate_chambers_across_strata(self):
        ch1 = self.gen.generate_chamber(1)
        self.assertEqual(ch1.stratum, "Prime Foundations")
        self.assertEqual(ch1.width, 8)
        self.assertEqual(ch1.height, 8)
        self.assertIsNotNone(ch1.relic_id)
        self.assertIn("43.7 Hz", ch1.narrative_liturgy)

        ch15 = self.gen.generate_chamber(15)
        self.assertEqual(ch15.stratum, "Inner Mandala")

        ch25 = self.gen.generate_chamber(25)
        self.assertEqual(ch25.stratum, "Outer Choirs")

        ch40 = self.gen.generate_chamber(40)
        self.assertEqual(ch40.stratum, "Shadow Canon")
        self.assertGreaterEqual(len(ch40.adversaries_spawn), 2)

    def test_export_json(self):
        data = self.gen.export_chamber_json(1)
        self.assertEqual(data["chamber_index"], 1)
        self.assertIn("tiles", data)
        self.assertIn("narrative_liturgy", data)
        self.assertEqual(len(data["tiles"]), 8)

class TestSaveManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_save.db")
        self.mgr = SaveManagerEngine(db_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_slot(self):
        sample_state = {"player": {"name": "Kiri Vespera", "hp": 20, "chamber": 1, "stratum": "Prime Foundations"}}
        res = self.mgr.save_slot(1, "Checkpoint Alpha", sample_state)
        self.assertTrue(res["success"])
        self.assertTrue(res["merkle_root"].startswith("0x"))

        loaded = self.mgr.load_slot(1)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["character_name"], "Kiri Vespera")
        self.assertEqual(loaded["state"]["player"]["hp"], 20)

    def test_list_slots(self):
        slots = self.mgr.list_slots()
        self.assertEqual(len(slots), 3)

    def test_export_chronicle(self):
        out_path = os.path.join(self.temp_dir, "test_chronicle.md")
        res_file = self.mgr.export_chronicle_to_markdown(out_path)
        self.assertTrue(os.path.exists(res_file))
        with open(res_file, "r") as f:
            content = f.read()
            self.assertIn("MLAOS-Prime", content)
            self.assertIn("Liturgy of State", content)

class TestCharacterCreation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_char.db")
        self.ledger_path = os.path.join(self.temp_dir, "test_ledger.ndjson")
        self.engine = CharacterCreationEngine(db_path=self.db_path, ledger_path=self.ledger_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_catalogs(self):
        self.assertEqual(len(self.engine.origins), 4)
        self.assertEqual(len(self.engine.archetypes), 4)
        self.assertEqual(len(self.engine.relics), 4)

    def test_create_character_stats_and_persistence(self):
        res = self.engine.create_character(
            character_name="TestHero",
            origin_key="HARMONIC_CANTOR",
            archetype_key="VOID_WALKER",
            spectrum_key="Gold",
            starter_relic_id="OBJ_AWAKENING_TOPAZ"
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["character_name"], "TestHero")
        self.assertTrue(res["genesis_merkle_root"].startswith("0x"))
        self.assertGreater(res["stats"]["resonance"], 5)

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        party_row = conn.execute("SELECT * FROM party WHERE name = 'TestHero'").fetchone()
        self.assertIsNotNone(party_row)
        prog_row = conn.execute("SELECT * FROM character_progression WHERE character_name = 'TestHero'").fetchone()
        self.assertIsNotNone(prog_row)
        conn.close()

        self.assertTrue(os.path.exists(self.ledger_path))
        with open(self.ledger_path, "r") as f:
            lines = f.readlines()
            self.assertGreaterEqual(len(lines), 1)

class TestUniverseAtlasEngine(unittest.TestCase):
    def setUp(self):
        self.atlas = UniverseAtlasEngine()

    def test_telemetry_and_constants(self):
        tel = self.atlas.get_telemetry()
        self.assertIn("Olney", tel.get("prime_geodetic_anchor", ""))
        self.assertEqual(tel.get("carrier_frequency_hz"), 43.7)

    def test_decalogue_laws(self):
        laws = self.atlas.get_laws()
        self.assertEqual(len(laws), 10)
        self.assertEqual(laws[0]["lex"], "Lex I")

    def test_heart_oculus_chambers(self):
        rings = self.atlas.get_heart_oculus_rings()
        self.assertEqual(len(rings["ring_1_sensory"]), 12)
        self.assertEqual(len(rings["ring_2_emotional"]), 12)
        self.assertEqual(len(rings["ring_3_memory"]), 12)

    def test_sovereign_trikeys(self):
        keys = self.atlas.get_trikeys()
        self.assertEqual(len(keys), 3)

if __name__ == "__main__":
    unittest.main()
