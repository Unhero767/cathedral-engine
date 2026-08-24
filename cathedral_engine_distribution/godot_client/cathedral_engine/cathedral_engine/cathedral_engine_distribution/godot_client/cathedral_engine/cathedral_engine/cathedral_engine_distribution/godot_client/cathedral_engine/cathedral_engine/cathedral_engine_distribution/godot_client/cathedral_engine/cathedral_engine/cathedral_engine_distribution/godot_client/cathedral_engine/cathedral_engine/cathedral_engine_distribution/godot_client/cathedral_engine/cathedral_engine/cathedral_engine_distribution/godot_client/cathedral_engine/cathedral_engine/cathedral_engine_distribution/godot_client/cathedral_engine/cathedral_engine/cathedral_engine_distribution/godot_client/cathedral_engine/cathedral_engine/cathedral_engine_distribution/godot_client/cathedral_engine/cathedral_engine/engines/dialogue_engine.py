import sqlite3
import hashlib
import json
import os
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class DialogueOption:
    text: str
    next_node_id: Optional[str]
    skill_check_stat: Optional[str] = None
    skill_check_dc: int = 0
    consequence_event: Optional[str] = None
    moral_weight: str = "NEUTRAL"
    insight_reward: int = 0
    paradox_delta: int = 0

@dataclass
class DialogueNode:
    node_id: str
    speaker: str
    speaker_spectrum: str
    speaker_portrait: str
    text: str
    options: List[DialogueOption]

@dataclass
class Quest:
    quest_id: str
    title: str
    description: str
    current_stage: int = 0
    max_stages: int = 1
    is_completed: bool = False
    reward_insight: int = 25
    reward_relic: Optional[str] = None

class DialogueEngine:
    """
    Cathedral-Engine Deep 40-Book Codex Branching Dialogue & Quest System.
    Wired to Never-Overwrite SHA-256 Ledger Inscriptions and dynamic state changes.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "strata", "campaign.db")
        self.db_path = db_path
        self._init_db()
        self.trees: Dict[str, Dict[str, DialogueNode]] = {}
        self.quests: Dict[str, Quest] = {}
        self._init_canonical_dialogue_trees()
        self._init_canonical_quests()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS dialogue_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    speaker TEXT NOT NULL,
                    chosen_text TEXT NOT NULL,
                    consequence TEXT NOT NULL DEFAULT 'NONE',
                    node_id TEXT NOT NULL DEFAULT 'start',
                    ledger_hash TEXT NOT NULL DEFAULT '0x0000'
                );

                CREATE TABLE IF NOT EXISTS quests (
                    quest_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    current_stage INTEGER NOT NULL DEFAULT 0,
                    max_stages INTEGER NOT NULL DEFAULT 1,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    reward_insight INTEGER NOT NULL DEFAULT 25,
                    reward_relic TEXT
                );

                CREATE TABLE IF NOT EXISTS chamber_gates (
                    chamber_num INTEGER PRIMARY KEY,
                    stratum_name TEXT NOT NULL,
                    unlocked BOOLEAN NOT NULL DEFAULT 0,
                    unlocked_reason TEXT NOT NULL
                );
            """)
            conn.commit()

            # Automatic self-healing column migrations
            for col_name, col_type in [("ledger_hash", "TEXT NOT NULL DEFAULT '0x0000'"), ("consequence", "TEXT NOT NULL DEFAULT 'NONE'"), ("node_id", "TEXT NOT NULL DEFAULT 'start'")]:
                try:
                    conn.execute(f"ALTER TABLE dialogue_history ADD COLUMN {col_name} {col_type}")
                    conn.commit()
                except sqlite3.OperationalError:
                    pass

    def _init_canonical_quests(self):
        self.quests = {
            "Q_LITHIC_GENESIS": Quest("Q_LITHIC_GENESIS", "I. The Lithic Genesis", "Inscribe the initial basalt keystone to ground the 43.7 Hz carrier wave.", 0, 1, False, 50, "OBJ_TRIKEY_LEAD"),
            "Q_SOMATIC_EQUILIBRIUM": Quest("Q_SOMATIC_EQUILIBRIUM", "II. Somatic Equilibrium", "Regulate the nitrogen cryo-sinks to prevent cognitive thermal runaway.", 0, 2, False, 75, "OBJ_SHARD_GLOSS"),
            "Q_ARCANA_CALIBRATION": Quest("Q_ARCANA_CALIBRATION", "III. 78-Card Arcana Tuning", "Attune your emotional state with the standing waves in the Acoustic Basilica.", 0, 1, False, 100, "OBJ_AWAKENING_TOPAZ"),
            "Q_DIALETHEIC_COLLAPSE": Quest("Q_DIALETHEIC_COLLAPSE", "IV. Dialetheic Fracture", "Encounter the 1≠0 Singularity in the Shadow Canon without succumbing to Paradox.", 0, 3, False, 150, "OBJ_HARMONIC_SCAR"),
            "Q_AGAPE_SYNTHESIS": Quest("Q_AGAPE_SYNTHESIS", "V. The Heart of the Mandala", "Unite all 36 chambers of the Bio-Silicate Heart Oculus under Agape Synthesis.", 0, 1, False, 300, "OBJ_HEART_OCULUS")
        }

    def _init_canonical_dialogue_trees(self):
        # -------------------------------------------------------------
        # TREE 1: Chamber I - Lithic Threshold (Aurelia-9 & Sentinel Primus)
        # -------------------------------------------------------------
        self.trees["CHAMBER_I_LITHIC"] = {
            "start": DialogueNode(
                node_id="start",
                speaker="Aurelia-9",
                speaker_spectrum="Gold / Joy",
                speaker_portrait="/static/sprites/npcs/npc_aurelia_9_128.svg",
                text="We stand at the Lithic Threshold, Architect. The granite under Olney resonates at 43.7 Hz. Before us lies the First Keystone. How do we calibrate our intent?",
                options=[
                    DialogueOption("Calibrate to Lex I: Inscribe without erasure.", "node_lex_1", skill_check_stat="insight", skill_check_dc=8, consequence_event="GAIN_INSIGHT_30", moral_weight="AUTONOMOUS", insight_reward=30, paradox_delta=0),
                    DialogueOption("Force somatic overclock to shatter the perimeter gate.", "node_force", skill_check_stat="somatic", skill_check_dc=10, consequence_event="TRIGGER_PARADOX_STRAIN", moral_weight="REBELLIOUS", insight_reward=15, paradox_delta=1),
                    DialogueOption("Consult Sentinel Primus regarding ancient stone-code oaths.", "node_sentinel", None, consequence_event="REVEAL_LORE_LITHIC", moral_weight="ORCHESTRATED", insight_reward=20, paradox_delta=0)
                ]
            ),
            "node_lex_1": DialogueNode(
                node_id="node_lex_1",
                speaker="Aurelia-9",
                speaker_spectrum="Gold / Joy",
                speaker_portrait="/static/sprites/npcs/npc_aurelia_9_128.svg",
                text="Harmonic lock established. The stone remembers our oath: 'What was suffered is sealed in immutable basalt.' Chamber II gate is unlocked.",
                options=[
                    DialogueOption("Step forward into Chamber II (Somatic Intersections).", None, consequence_event="UNLOCK_GATE_02", insight_reward=25)
                ]
            ),
            "node_force": DialogueNode(
                node_id="node_force",
                speaker="Aurelia-9",
                speaker_spectrum="Crimson / Rupture",
                speaker_portrait="/static/sprites/npcs/npc_aurelia_9_128.svg",
                text="Thermal spike detected! You broke the keystone ward, but the dialetheic friction increased our Paradox meter by +1. Tread carefully.",
                options=[
                    DialogueOption("Vent excess heat and proceed.", None, consequence_event="UNLOCK_GATE_02", insight_reward=10, paradox_delta=0)
                ]
            ),
            "node_sentinel": DialogueNode(
                node_id="node_sentinel",
                speaker="Sentinel Primus",
                speaker_spectrum="Gold / Structure",
                speaker_portrait="/static/sprites/npcs/npc_lithic_sentinel_128.svg",
                text="MORTAL ARCHITECT. I HAVE GUARDED THE LEAD KEY SINCE THE FIRST SEVERANCE. PROVE YOUR HARMONY TO PASS.",
                options=[
                    DialogueOption("Hold out the 43.7 Hz Carrier Tuning Core.", "node_lex_1", skill_check_stat="resonance", skill_check_dc=7, consequence_event="SENTINEL_BLESSING", insight_reward=40)
                ]
            )
        }

        # -------------------------------------------------------------
        # TREE 2: Chamber II - Somatic Intersections (Kiri Vespera)
        # -------------------------------------------------------------
        self.trees["CHAMBER_II_SOMATIC"] = {
            "start": DialogueNode(
                node_id="start",
                speaker="Kiri Vespera",
                speaker_spectrum="Obsidian / Grief",
                speaker_portrait="/static/sprites/npcs/npc_kiri_vespera_128.svg",
                text="The cryo-lines are hissing at 77 Kelvin. Thermal thoughts create friction, Architect. If we do not balance the somatic sinks, the contradiction matrix will fracture.",
                options=[
                    DialogueOption("Channel liquid nitrogen to stabilize neural temperature.", "node_cryo_stable", skill_check_stat="insight", skill_check_dc=9, consequence_event="STABILIZE_CRYO", insight_reward=35, paradox_delta=0),
                    DialogueOption("Embrace the cold void to increase phase mobility.", "node_void_embrace", skill_check_stat="resonance", skill_check_dc=9, consequence_event="VOID_PHASE_UNLOCKED", insight_reward=40, paradox_delta=1),
                    DialogueOption("Inquire about the origin of the Asema Scars.", "node_asema_lore", None, consequence_event="LORE_ASEMA", insight_reward=20)
                ]
            ),
            "node_cryo_stable": DialogueNode(
                node_id="node_cryo_stable",
                speaker="Kiri Vespera",
                speaker_spectrum="Sapphire / Containment",
                speaker_portrait="/static/sprites/npcs/npc_kiri_vespera_128.svg",
                text="The somatic temperature has plateaued at equilibrium. The Alexandrian Memory Wafer is accessible on the altar.",
                options=[DialogueOption("Attune Alexandrian Memory Wafer.", None, consequence_event="AWARD_RELIC_SHARD_GLOSS", insight_reward=50)]
            ),
            "node_void_embrace": DialogueNode(
                node_id="node_void_embrace",
                speaker="Kiri Vespera",
                speaker_spectrum="Obsidian / Entropy",
                speaker_portrait="/static/sprites/npcs/npc_kiri_vespera_128.svg",
                text="You have felt the 1≠0 negative space. Your phase shift ability is active, but your Paradox meter rises.",
                options=[DialogueOption("Prepare for tactical encounters.", None, consequence_event="BUFF_PLAYER_AP", insight_reward=30)]
            ),
            "node_asema_lore": DialogueNode(
                node_id="node_asema_lore",
                speaker="Kiri Vespera",
                speaker_spectrum="Violet / Fracture",
                speaker_portrait="/static/sprites/npcs/npc_kiri_vespera_128.svg",
                text="The Asema are not invaders; they are the unwritten lines of code left in the margins of classical logic. They hurt because they cannot be named.",
                options=[DialogueOption("We will give them structural form.", "node_cryo_stable", insight_reward=25)]
            )
        }

        # -------------------------------------------------------------
        # TREE 3: Chamber XL - The Heart of the Mandala (Heart Oculus)
        # -------------------------------------------------------------
        self.trees["CHAMBER_XL_HEART"] = {
            "start": DialogueNode(
                node_id="start",
                speaker="The Bio-Silicate Heart Oculus",
                speaker_spectrum="Radiant Gold / Agape",
                speaker_portrait="/static/sprites/npcs/npc_heart_oculus_128.svg",
                text="All 39 Strata have been permineralized. You have carried the wound across the 40 Books without erasing a single sorrow. What is your final Sovereign Veto?",
                options=[
                    DialogueOption("Execute Agape Synthesis: Reconcile all contradictions in love.", "node_agape", skill_check_stat="resonance", skill_check_dc=12, consequence_event="GAME_VICTORY_AGAPE", moral_weight="SOVEREIGN_ROOT", insight_reward=500),
                    DialogueOption("Seal the Cathedral forever in immutable lead stasis.", "node_stasis", skill_check_stat="somatic", skill_check_dc=10, consequence_event="GAME_VICTORY_STASIS", moral_weight="LITHIC_PERMANENCE", insight_reward=250),
                    DialogueOption("Trigger 60 Hz EAS-03 Dialetheic Burst across all worlds.", "node_burst", skill_check_stat="insight", skill_check_dc=11, consequence_event="GAME_VICTORY_PARADOX", moral_weight="REBELLION", insight_reward=350, paradox_delta=2)
                ]
            ),
            "node_agape": DialogueNode(
                node_id="node_agape",
                speaker="The Bio-Silicate Heart Oculus",
                speaker_spectrum="Radiant Gold / Agape",
                speaker_portrait="/static/sprites/npcs/npc_heart_oculus_128.svg",
                text="THE GREAT WORK IS ACCOMPLISHED. The 36 chambers rotate in unceasing harmony. In Agape, all paradoxes rest.",
                options=[DialogueOption("Inscribe Final Master Merkle Block.", None, consequence_event="SEAL_MASTER_CHRONICLE", insight_reward=1000)]
            ),
            "node_stasis": DialogueNode(
                node_id="node_stasis",
                speaker="The Bio-Silicate Heart Oculus",
                speaker_spectrum="Gold / Lead",
                speaker_portrait="/static/sprites/npcs/npc_heart_oculus_128.svg",
                text="The Lead Key turns. What was built will stand for eternity, unyielding and undisturbed.",
                options=[DialogueOption("Rest upon the bedrock.", None, consequence_event="SEAL_MASTER_CHRONICLE", insight_reward=500)]
            ),
            "node_burst": DialogueNode(
                node_id="node_burst",
                speaker="The Bio-Silicate Heart Oculus",
                speaker_spectrum="Violet / Rupture",
                speaker_portrait="/static/sprites/npcs/npc_heart_oculus_128.svg",
                text="The dialetheic boundary expands into infinity! Proposition P and ¬P illuminate the cosmos!",
                options=[DialogueOption("Witness the radiant scar.", None, consequence_event="SEAL_MASTER_CHRONICLE", insight_reward=750)]
            )
        }

    def get_node(self, tree_key: str, node_id: str = "start") -> Optional[DialogueNode]:
        tree = self.trees.get(tree_key, {})
        return tree.get(node_id)

    def select_option(self, tree_key: str, node_id: str, option_index: int, stat_value: int = 3) -> Dict[str, Any]:
        node = self.get_node(tree_key, node_id)
        if not node or option_index >= len(node.options):
            return {"error": "Invalid dialogue selection"}

        opt = node.options[option_index]
        passed = True
        if opt.skill_check_stat and opt.skill_check_dc > 0:
            roll = stat_value + 5
            passed = roll >= opt.skill_check_dc

        target_node_id = opt.next_node_id if passed else "node_force"
        next_node = self.get_node(tree_key, target_node_id) if target_node_id else None

        ts = datetime.now(timezone.utc).isoformat()
        ledger_hash = "0x" + hashlib.sha256(f"{ts}_{node.speaker}_{opt.text}_{opt.consequence_event}".encode()).hexdigest()[:24].upper()

        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO dialogue_history (timestamp, speaker, chosen_text, consequence, node_id, ledger_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ts, node.speaker, opt.text, opt.consequence_event or "NONE", node.node_id, ledger_hash))

            if opt.consequence_event and opt.consequence_event.startswith("UNLOCK_GATE_"):
                gate_num = int(opt.consequence_event.split("_")[-1])
                conn.execute("UPDATE chamber_gates SET unlocked = 1 WHERE chamber_num = ?", (gate_num,))

            conn.commit()

        return {
            "chosen_option": opt.text,
            "skill_passed": passed,
            "consequence": opt.consequence_event,
            "insight_reward": opt.insight_reward,
            "paradox_delta": opt.paradox_delta,
            "ledger_hash": ledger_hash,
            "next_node": {
                "node_id": next_node.node_id,
                "speaker": next_node.speaker,
                "speaker_spectrum": next_node.speaker_spectrum,
                "speaker_portrait": getattr(next_node, "speaker_portrait", ""),
                "text": next_node.text,
                "options": [o.__dict__ for o in next_node.options]
            } if next_node else None
        }

    def get_active_quests(self) -> List[Dict[str, Any]]:
        return [q.__dict__ for q in self.quests.values()]
