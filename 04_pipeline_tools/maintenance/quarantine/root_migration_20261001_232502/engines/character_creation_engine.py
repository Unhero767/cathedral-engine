import json
import sqlite3
import os
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

@dataclass
class OriginVector:
    key: str
    name: str
    stratum: str
    lore: str
    stat_bonuses: Dict[str, int]
    passive_trait: str
    description: str

@dataclass
class CharacterArchetype:
    key: str
    name: str
    default_spectrum: str
    starter_weapon: str
    stat_modifiers: Dict[str, int]
    description: str

@dataclass
class StarterRelic:
    id: str
    name: str
    strain_weight: float
    stat_bonus: Dict[str, int]
    description: str

class CharacterCreationEngine:
    """
    Cathedral-Engine Narrative Character Creation Engine
    Weaves player origin vectors into the 40-Book Codex strata, calculates base stats,
    attunes 128px HD starter relics, and permanently inscribes genesis into the Ash Ledger.
    """
    def __init__(self, db_path: Optional[str] = None, ledger_path: Optional[str] = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if db_path is None:
            db_path = os.path.join(base_dir, "strata", "campaign.db")
        if ledger_path is None:
            ledger_path = os.path.join(base_dir, "strata", "prime_ledger.ndjson")
        self.db_path = db_path
        self.ledger_path = ledger_path
        self.origins = self._init_origins()
        self.archetypes = self._init_archetypes()
        self.relics = self._init_starter_relics()
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS party (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    designation TEXT NOT NULL,
                    emotional_state TEXT NOT NULL,
                    paradox INTEGER NOT NULL DEFAULT 0,
                    hp INTEGER NOT NULL DEFAULT 20
                );

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

    def _init_origins(self) -> Dict[str, OriginVector]:
        return {
            "LITHIC_SCION": OriginVector(
                key="LITHIC_SCION",
                name="Lithic Scion (Prime Foundations, Books I–X)",
                stratum="Prime Foundations",
                lore="Born from the permineralized granite strata beneath Olney, IL. Your flesh bears ancient stone-code equations oscillating at 43.7 Hz.",
                stat_bonuses={"max_hp": 4, "somatic": 2, "resonance": 1},
                passive_trait="Permineralized_Carapace (Takes 2 reduced kinetic damage from physical strikes)",
                description="High durability and resistance to somatic trauma."
            ),
            "SYNTHETIC_SYNTHETE": OriginVector(
                key="SYNTHETIC_SYNTHETE",
                name="Synthetic Synthete (Inner Mandala, Books XI–XX)",
                stratum="Inner Mandala",
                lore="Engineered with cybernetic neural threading and integrated cryo-coolant lines. You perceive reality through cognitive geometry.",
                stat_bonuses={"max_ap": 1, "insight": 2, "resonance": 1},
                passive_trait="Somatic_Cryo_Sink (Can vent 2 excess heat without triggering Paradox gain)",
                description="High AP flexibility and mathematical problem-solving."
            ),
            "HARMONIC_CANTOR": OriginVector(
                key="HARMONIC_CANTOR",
                name="Harmonic Cantor (Outer Choirs, Books XXI–XXX)",
                stratum="Outer Choirs",
                lore="Initiated in the sacred acoustic basilicas. Your voice aligns with standing waves to command the 78-Card Ignition Arcana.",
                stat_bonuses={"resonance": 3, "insight": 1, "unspent_insight": 50},
                passive_trait="Carrier_Harmony (+2 bonus on all 2d6 Arcana action resolution rolls)",
                description="Exceptional spiritual resonance and high action roll consistency."
            ),
            "ASEMA_EXILE": OriginVector(
                key="ASEMA_EXILE",
                name="Asema Exile (Shadow Canon, Books XXXI–XL)",
                stratum="Shadow Canon",
                lore="A survivor of the dialetheic boundary who has looked into the 1≠0 negative space. Contradiction is your natural element.",
                stat_bonuses={"resonance": 2, "somatic": 1, "insight": 1},
                passive_trait="Phase_Drift (Paradox Break threshold raised from 5 to 7; can phase through monoliths)",
                description="Unmatched tolerance for paradox and ability to traverse blocked terrain."
            )
        }

    def _init_archetypes(self) -> Dict[str, CharacterArchetype]:
        return {
            "VOID_WALKER": CharacterArchetype(
                key="VOID_WALKER",
                name="Void Walker",
                default_spectrum="Obsidian",
                starter_weapon="Phase-Shift Void Dagger",
                stat_modifiers={"resonance": 2, "max_ap": 1},
                description="A master of entropy and space inversion who channels Paradox into lethal burst damage."
            ),
            "CYBERNETIC_SYNTHETE": CharacterArchetype(
                key="CYBERNETIC_SYNTHETE",
                name="Cybernetic Synthete",
                default_spectrum="Sapphire",
                starter_weapon="High-Frequency Permineralized Monoblade",
                stat_modifiers={"somatic": 2, "insight": 1},
                description="A high-speed melee specialist wielding ceramic monoblades and somatic heat sinks."
            ),
            "LITHIC_ANCHOR": CharacterArchetype(
                key="LITHIC_ANCHOR",
                name="Lithic Anchor",
                default_spectrum="Gold",
                starter_weapon="Resonator Granite Maul",
                stat_modifiers={"max_hp": 6, "somatic": 2},
                description="An immovable tank holding choke points, radiating seismic waves, and buffing armor."
            ),
            "CHOIR_CANTOR": CharacterArchetype(
                key="CHOIR_CANTOR",
                name="Choir Cantor",
                default_spectrum="Emerald",
                starter_weapon="Acoustic Harmonic Chime",
                stat_modifiers={"resonance": 2, "insight": 2},
                description="A ranged support mystic who commands acoustic frequencies to heal allies and disrupt enemies."
            )
        }

    def _init_starter_relics(self) -> Dict[str, StarterRelic]:
        return {
            "OBJ_TRIKEY_LEAD": StarterRelic(
                id="OBJ_TRIKEY_LEAD",
                name="Lead Key of Duration (Saturn / Permineralization)",
                strain_weight=2.0,
                stat_bonus={"somatic": 2, "max_hp": 4},
                description="A brutalist lead key with gold wire inlays, grounding the user in physical stone permanence."
            ),
            "OBJ_SHARD_GLOSS": StarterRelic(
                id="OBJ_SHARD_GLOSS",
                name="Alexandrian Cryptographic Memory Chip",
                strain_weight=1.0,
                stat_bonus={"insight": 2, "unspent_insight": 50},
                description="A translucent glass wafer inscribed with golden High-Pali code lines, enhancing cognitive retrieval."
            ),
            "OBJ_AWAKENING_TOPAZ": StarterRelic(
                id="OBJ_AWAKENING_TOPAZ",
                name="Lithic Summa Golden-Ratio Shard",
                strain_weight=1.5,
                stat_bonus={"resonance": 2, "insight": 1},
                description="A dodecahedral amber topaz shard proportioned to Phi=1.62, refracting internal mathematical equations."
            ),
            "OBJ_LUMEN_LANTERN": StarterRelic(
                id="OBJ_LUMEN_LANTERN",
                name="The Lantern at the Edge of Memory",
                strain_weight=1.5,
                stat_bonus={"max_hp": 6, "resonance": 1},
                description="A cathedral brass lantern enclosing a levitating gold-indigo Lumen core that illuminates hidden truth."
            )
        }

    def create_character(
        self,
        character_name: str,
        origin_key: str = "LITHIC_SCION",
        archetype_key: str = "VOID_WALKER",
        spectrum_key: str = "Gold",
        starter_relic_id: str = "OBJ_TRIKEY_LEAD"
    ) -> Dict[str, Any]:
        """
        Creates and registers a new character instance, computing total stats from origin + archetype + relic,
        inscribing into SQLite and stamping the Genesis block into prime_ledger.ndjson.
        """
        origin = self.origins.get(origin_key, self.origins["LITHIC_SCION"])
        arch = self.archetypes.get(archetype_key, self.archetypes["VOID_WALKER"])
        relic = self.relics.get(starter_relic_id, self.relics["OBJ_TRIKEY_LEAD"])

        # Base Stats
        base_hp = 20 + origin.stat_bonuses.get("max_hp", 0) + arch.stat_modifiers.get("max_hp", 0) + relic.stat_bonus.get("max_hp", 0)
        base_ap = 4 + origin.stat_bonuses.get("max_ap", 0) + arch.stat_modifiers.get("max_ap", 0)
        resonance = 3 + origin.stat_bonuses.get("resonance", 0) + arch.stat_modifiers.get("resonance", 0) + relic.stat_bonus.get("resonance", 0)
        somatic = 2 + origin.stat_bonuses.get("somatic", 0) + arch.stat_modifiers.get("somatic", 0) + relic.stat_bonus.get("somatic", 0)
        insight = 3 + origin.stat_bonuses.get("insight", 0) + arch.stat_modifiers.get("insight", 0) + relic.stat_bonus.get("insight", 0)
        unspent_xp = 100 + origin.stat_bonuses.get("unspent_insight", 0) + relic.stat_bonus.get("unspent_insight", 0)
        max_strain = 6.0

        ts = datetime.now(timezone.utc).isoformat()
        genesis_hash = "0x" + hashlib.sha256(f"GENESIS_{character_name}_{origin_key}_{archetype_key}_{ts}".encode()).hexdigest().upper()

        with self._get_conn() as conn:
            # 1. Inscribe Party Record
            conn.execute("""
                INSERT OR REPLACE INTO party (name, designation, emotional_state, paradox, hp)
                VALUES (?, ?, ?, 0, ?)
            """, (character_name, f"{arch.name} ({origin.stratum})", f"{spectrum_key}/Joy", base_hp))
            party_id = conn.execute("SELECT id FROM party WHERE name = ?", (character_name,)).fetchone()[0]

            # 2. Inscribe Progression Stats
            conn.execute("""
                INSERT OR REPLACE INTO character_progression (character_name, level, insight_xp, unspent_insight, resonance, somatic, insight, max_hp, max_ap, max_strain)
                VALUES (?, 1, 0, ?, ?, ?, ?, ?, ?, ?)
            """, (character_name, unspent_xp, resonance, somatic, insight, base_hp, base_ap, max_strain))

            # 3. Inscribe Starter Relic
            conn.execute("""
                INSERT INTO inventory (owner_id, item_name, item_class, attuned, strain_weight)
                VALUES (?, ?, 'Relic', 1, ?)
            """, (party_id, relic.name, relic.strain_weight))

            conn.commit()

        # Inscribe Genesis Block to prime_ledger.ndjson
        if os.path.exists(os.path.dirname(self.ledger_path)):
            genesis_event = {
                "event_type": "CHARACTER_GENESIS",
                "character_name": character_name,
                "origin_stratum": origin.stratum,
                "archetype": arch.name,
                "spectrum": spectrum_key,
                "attuned_relic": relic.name,
                "timestamp": ts,
                "merkle_genesis_root": genesis_hash
            }
            nl = chr(10)
            with open(self.ledger_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(genesis_event) + nl)

        return {
            "success": True,
            "character_name": character_name,
            "origin": origin.name,
            "archetype": arch.name,
            "spectrum": spectrum_key,
            "passive_trait": origin.passive_trait,
            "starter_weapon": arch.starter_weapon,
            "attuned_relic": relic.name,
            "stats": {
                "max_hp": base_hp,
                "max_ap": base_ap,
                "resonance": resonance,
                "somatic": somatic,
                "insight": insight,
                "unspent_insight": unspent_xp
            },
            "genesis_merkle_root": genesis_hash,
            "timestamp": ts
        }

if __name__ == "__main__":
    engine = CharacterCreationEngine()
    print("[CHARACTER CREATION] Initialized. Testing creation for 'Kenneth Dallmier'...")
    res = engine.create_character(
        character_name="Kenneth Dallmier",
        origin_key="HARMONIC_CANTOR",
        archetype_key="VOID_WALKER",
        spectrum_key="Gold",
        starter_relic_id="OBJ_AWAKENING_TOPAZ"
    )
    print("Genesis Inscription Result:")
    print(json.dumps(res, indent=2))
