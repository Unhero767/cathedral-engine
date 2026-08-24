import sqlite3
import os
import random
import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class Talent:
    id: str
    name: str
    tier: int
    cost_insight: int
    spectrum_affinity: str
    description: str
    stat_modifiers: Dict[str, int]
    is_unlocked: bool = False

@dataclass
class RelicRecipe:
    recipe_id: str
    result_name: str
    result_class: str
    strain_weight: float
    required_materials: Dict[str, int]
    stat_bonus: Dict[str, int]
    description: str

class ProgressionEngine:
    """
    Cathedral-Engine Character Progression & Relic Crafting Engine
    Manages Insight XP leveling, talent tree nodes, relic forging, and inventory strain.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "strata", "campaign.db")
        self.db_path = db_path
        self._init_db()
        self.talent_trees = self._init_talents()
        self.recipes = self._init_recipes()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS character_progression (
                    character_name TEXT PRIMARY KEY,
                    level INTEGER NOT NULL DEFAULT 1,
                    insight_xp INTEGER NOT NULL DEFAULT 0,
                    unspent_insight INTEGER NOT NULL DEFAULT 100,
                    resonance INTEGER NOT NULL DEFAULT 3,
                    somatic INTEGER NOT NULL DEFAULT 2,
                    insight INTEGER NOT NULL DEFAULT 3,
                    max_hp INTEGER NOT NULL DEFAULT 20,
                    max_ap INTEGER NOT NULL DEFAULT 4,
                    max_strain REAL NOT NULL DEFAULT 6.0
                );

                CREATE TABLE IF NOT EXISTS inventory_materials (
                    material_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0,
                    category TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS character_talents (
                    character_name TEXT NOT NULL,
                    talent_id TEXT NOT NULL,
                    unlocked_at TEXT NOT NULL,
                    PRIMARY KEY(character_name, talent_id)
                );

                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER,
                    item_name TEXT NOT NULL,
                    item_class TEXT NOT NULL,
                    attuned BOOLEAN NOT NULL DEFAULT 0,
                    strain_weight REAL NOT NULL DEFAULT 1.0
                );
            """)
            conn.commit()

            # Seed progression and materials if empty
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as cnt FROM character_progression")
            if cur.fetchone()["cnt"] == 0:
                self.seed_defaults()

    def seed_defaults(self):
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO character_progression (character_name, level, insight_xp, unspent_insight, resonance, somatic, insight, max_hp, max_ap, max_strain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ("Kiri Vespera", 1, 150, 150, 4, 3, 3, 20, 4, 6.0))

            conn.execute("""
                INSERT INTO character_progression (character_name, level, insight_xp, unspent_insight, resonance, somatic, insight, max_hp, max_ap, max_strain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ("Aurelia-9", 1, 100, 100, 3, 4, 4, 25, 4, 8.0))

            # Materials
            materials = [
                ("MAT_LITHIC_STONE", "Permineralized Granite", 12, "Mineral"),
                ("MAT_LUMEN_CORE", "Lumen Core (Gold)", 3, "Energy"),
                ("MAT_PRISM_SHARD", "Resonance Prism Shard", 5, "Catalyst"),
                ("MAT_OBSIDIAN_ASH", "Permineralized Ash", 8, "Catalyst")
            ]
            conn.executemany("INSERT OR IGNORE INTO inventory_materials VALUES (?, ?, ?, ?)", materials)
            conn.commit()

    def _init_talents(self) -> Dict[str, List[Talent]]:
        return {
            "Void Walker": [
                Talent("T_VOID_SURGE", "Void Inversion Surge", 1, 50, "Obsidian", "Channel paradox directly into bonus movement (+1 AP).", {"max_ap": 1}),
                Talent("T_PHASE_DRIFT", "Phase Drift", 1, 50, "Teal", "Ignore terrain movement penalties on A-Field thermal tiles.", {"somatic": 1}),
                Talent("T_DIALETHEIC_ABSORB", "Dialetheic Absorption", 2, 100, "Sapphire", "When hit by an attack, reduce damage by 3 and gain +1 Resonance.", {"resonance": 2}),
                Talent("T_PARADOX_MASTERY", "Paradox Equilibrium", 3, 150, "Gold", "Paradox Break limit increased from 5 to 7.", {"max_hp": 5})
            ],
            "Cybernetic Synthete": [
                Talent("T_MONO_OVERCLOCK", "Monoblade Overclock", 1, 50, "Crimson", "Monoblade strikes deal +3 damage.", {"somatic": 2}),
                Talent("T_SOMATIC_COOLING", "Somatic Heat Dispersal", 1, 50, "Blue", "Heat sinks vent 40% faster, preventing somatic burn.", {"max_strain": 2}),
                Talent("T_TRI_KEY_AUTH", "Tri-Key Sovereignty", 2, 100, "Gold", "Grants immunity to cognitive logic storms.", {"insight": 2}),
                Talent("T_AUTOPOIETIC_FRAME", "Autopoietic Permineralization", 3, 150, "Emerald", "Regenerate 4 HP at the beginning of each combat round.", {"max_hp": 8})
            ]
        }

    def _init_recipes(self) -> Dict[str, RelicRecipe]:
        return {
            "RECIPE_HGASE_PRISM": RelicRecipe(
                recipe_id="RECIPE_HGASE_PRISM",
                result_name="Refined HGASE Resonator Prism",
                result_class="Relic",
                strain_weight=2.0,
                required_materials={"MAT_LITHIC_STONE": 4, "MAT_PRISM_SHARD": 2, "MAT_LUMEN_CORE": 1},
                stat_bonus={"resonance": 2, "insight": 1},
                description="A polished chromatic prism harmonizing A-Field standing waves."
            ),
            "RECIPE_MONOBLADE": RelicRecipe(
                recipe_id="RECIPE_MONOBLADE",
                result_name="High-Frequency Permineralized Monoblade",
                result_class="Weapon",
                strain_weight=1.5,
                required_materials={"MAT_LITHIC_STONE": 6, "MAT_OBSIDIAN_ASH": 3, "MAT_LUMEN_CORE": 1},
                stat_bonus={"somatic": 3},
                description="A nanostructured ceramic blade oscillating at 43.7 Hz."
            ),
            "RECIPE_SOMATIC_HEATSINK": RelicRecipe(
                recipe_id="RECIPE_SOMATIC_HEATSINK",
                result_name="Somatic Cryo-Heat Sink",
                result_class="Relic",
                strain_weight=1.0,
                required_materials={"MAT_LITHIC_STONE": 3, "MAT_OBSIDIAN_ASH": 4},
                stat_bonus={"max_hp": 5, "max_strain": 1},
                description="Absorbs and dissipates thermal energy during high-load dialectic collisions."
            )
        }

    def get_character_stats(self, char_name: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT * FROM character_progression WHERE character_name = ?", (char_name,))
            row = cur.fetchone()
            if not row:
                return None
            return dict(row)

    def unlock_talent(self, char_name: str, talent_id: str, archetype: str) -> Dict[str, Any]:
        """Unlocks a talent node if character has sufficient unspent insight points."""
        stats = self.get_character_stats(char_name)
        if not stats:
            return {"error": "Character not found"}

        talents = self.talent_trees.get(archetype, [])
        talent = next((t for t in talents if t.id == talent_id), None)
        if not talent:
            return {"error": "Talent not found"}

        if stats["unspent_insight"] < talent.cost_insight:
            return {"error": f"Insufficient Insight points (Requires {talent.cost_insight}, has {stats['unspent_insight']})"}

        set_clauses = ["unspent_insight = unspent_insight - ?"]
        params = [talent.cost_insight]

        for stat, mod in talent.stat_modifiers.items():
            set_clauses.append(f"{stat} = {stat} + ?")
            params.append(mod)

        params.append(char_name)
        sql = f"UPDATE character_progression SET {', '.join(set_clauses)} WHERE character_name = ?"

        with self._get_conn() as conn:
            conn.execute(sql, params)
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            conn.execute("INSERT OR REPLACE INTO character_talents VALUES (?, ?, ?)", (char_name, talent_id, ts))
            conn.commit()

        return {
            "success": True,
            "unlocked_talent": talent.name,
            "stat_bonuses": talent.stat_modifiers,
            "remaining_insight": stats["unspent_insight"] - talent.cost_insight
        }

    def craft_relic(self, recipe_id: str, owner_id: int) -> Dict[str, Any]:
        """Crafts a relic item if required inventory materials are available."""
        recipe = self.recipes.get(recipe_id)
        if not recipe:
            return {"error": "Recipe not found"}

        with self._get_conn() as conn:
            # Verify materials
            for mat_id, req_qty in recipe.required_materials.items():
                cur = conn.execute("SELECT quantity FROM inventory_materials WHERE material_id = ?", (mat_id,))
                row = cur.fetchone()
                if not row or row["quantity"] < req_qty:
                    return {"error": f"Missing material: {mat_id} (Requires {req_qty})"}

            # Deduct materials
            for mat_id, req_qty in recipe.required_materials.items():
                conn.execute("UPDATE inventory_materials SET quantity = quantity - ? WHERE material_id = ?", (req_qty, mat_id))

            # Inscribe relic into inventory
            conn.execute("""
                INSERT INTO inventory (owner_id, item_name, item_class, attuned, strain_weight)
                VALUES (?, ?, ?, 1, ?)
            """, (owner_id, recipe.result_name, recipe.result_class, recipe.strain_weight))
            conn.commit()

        return {
            "success": True,
            "crafted_item": recipe.result_name,
            "class": recipe.result_class,
            "strain_weight": recipe.strain_weight,
            "stat_bonuses": recipe.stat_bonus
        }

if __name__ == "__main__":
    prog = ProgressionEngine()
    stats = prog.get_character_stats("Kiri Vespera")
    print(f"[PROGRESSION] Character: {stats['character_name']} (Lvl {stats['level']}) | Insight XP: {stats['unspent_insight']}")
    res = prog.unlock_talent("Kiri Vespera", "T_VOID_SURGE", "Void Walker")
    print(f"  Talent Unlock Result: {res}")
    craft = prog.craft_relic("RECIPE_HGASE_PRISM", owner_id=1)
    print(f"  Crafting Result: {craft}")
