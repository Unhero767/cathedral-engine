import random
import os
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple

from .paraconsistent_engine import EAS03ParaconsistentEngine
from .emotional_physics_engine import EmotionalPhysicsEngine
from .arcana_engine import ArcanaEngine
from .enemy_engine import EnemyEngine, EnemyInstance, EnemySpectrum
from .dialogue_engine import DialogueEngine
from .progression_engine import ProgressionEngine
from .campaign_engine import CampaignEngine

class GameState(str, Enum):
    EXPLORATION = "EXPLORATION"
    DIALOGUE = "DIALOGUE"
    TACTICAL_COMBAT = "TACTICAL_COMBAT"
    AFTERMATH_LOOT = "AFTERMATH_LOOT"
    SANCTUARY_REST = "SANCTUARY_REST"
    PARADOX_BREAK = "PARADOX_BREAK"

@dataclass
class PlayerSession:
    character_name: str
    archetype: str
    current_hp: int
    max_hp: int
    x: int = 1
    y: int = 1
    current_ap: int = 4
    max_ap: int = 4
    paradox: int = 0
    max_paradox: int = 5
    emotional_state: str = "Gold/Joy"
    spectrum_affinity: EnemySpectrum = EnemySpectrum.TEAL
    active_stratum: str = "Prime Foundations"
    chamber_index: int = 1

class GameLoopEngine:
    """
    Cathedral-Engine Master RPG State Machine & Turn Controller
    Orchestrates player exploration, interactive dialogue, tactical grid combat,
    adversary AI turns with chromatic affinities, and character progression.
    """
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.base_dir = base_dir
        self.state = GameState.EXPLORATION

        # Instantiate Subsystems
        self.paraconsistent = EAS03ParaconsistentEngine(os.path.join(base_dir, "strata", "prime_ledger.ndjson"))
        self.physics = EmotionalPhysicsEngine()
        self.arcana = ArcanaEngine()
        self.enemies = EnemyEngine()
        self.dialogue = DialogueEngine(os.path.join(base_dir, "strata", "campaign.db"))
        self.progression = ProgressionEngine(os.path.join(base_dir, "strata", "campaign.db"))
        self.campaign = CampaignEngine(os.path.join(base_dir, "strata", "campaign.db"))

        # Active Session State
        self.player = PlayerSession("Kiri Vespera", "Void Walker", 20, 20, x=1, y=1, spectrum_affinity=EnemySpectrum.OBSIDIAN)
        self.active_combat_squad: List[EnemyInstance] = []
        self.grid_width = 8
        self.grid_height = 8
        self.turn_counter = 1
        self.action_log: List[str] = []

    def start_new_game(self, character_name: str = "Kiri Vespera", archetype: str = "Void Walker") -> Dict[str, Any]:
        """Initializes a fresh RPG adventure in Chamber I."""
        affinity = EnemySpectrum.OBSIDIAN if archetype == "Void Walker" else EnemySpectrum.GOLD
        self.player = PlayerSession(character_name, archetype, 20, 20, x=1, y=1, spectrum_affinity=affinity)
        self.state = GameState.EXPLORATION
        self.active_combat_squad = []
        self.turn_counter = 1
        self.action_log = [f"Game initialized for {character_name} ({archetype}) at the Lithic Threshold."]
        
        return self.get_full_game_state()

    def get_full_game_state(self) -> Dict[str, Any]:
        """Returns complete serializable game state for Web Client and CLI renderers."""
        return {
            "game_state": self.state.value,
            "turn": self.turn_counter,
            "player": {
                "name": self.player.character_name,
                "archetype": self.player.archetype,
                "hp": self.player.current_hp,
                "max_hp": self.player.max_hp,
                "ap": self.player.current_ap,
                "max_ap": self.player.max_ap,
                "paradox": self.player.paradox,
                "max_paradox": self.player.max_paradox,
                "emotional_state": self.player.emotional_state,
                "spectrum": self.player.spectrum_affinity.value,
                "x": self.player.x,
                "y": self.player.y,
                "stratum": self.player.active_stratum,
                "chamber": self.player.chamber_index
            },
            "enemies": [
                {
                    "uid": e.uid,
                    "name": e.name,
                    "archetype": e.archetype,
                    "spectrum": e.spectrum.value,
                    "hp": e.current_hp,
                    "max_hp": e.max_hp,
                    "armor": e.armor,
                    "x": e.x,
                    "y": e.y,
                    "ap": e.ap,
                    "passive": e.passive_trait,
                    "is_overdriven": e.is_overdriven,
                    "is_petrified": e.is_petrified,
                    "is_alive": e.is_alive
                }
                for e in self.active_combat_squad
            ],
            "action_log": self.action_log[-8:],
            "active_quests": self.dialogue.get_active_quests()
        }

    def player_move(self, target_x: int, target_y: int) -> Dict[str, Any]:
        """Handles player movement on the tactical grid."""
        if not (0 <= target_x < self.grid_width and 0 <= target_y < self.grid_height):
            return {"error": "Out of bounds movement."}

        # Check combat AP cost
        if self.state == GameState.TACTICAL_COMBAT:
            if self.player.current_ap < 1:
                return {"error": "Insufficient Action Points (Requires 1 AP to move)."}
            self.player.current_ap -= 1

        self.player.x, self.player.y = target_x, target_y
        log_msg = f"Player moved to ({target_x}, {target_y})."
        self.action_log.append(log_msg)

        # Trigger random exploration encounter if moving onto trigger zones (e.g. x >= 4 in exploration)
        if self.state == GameState.EXPLORATION and target_x >= 4 and not self.active_combat_squad:
            self.trigger_combat_encounter()

        return self.get_full_game_state()

    def trigger_combat_encounter(self, difficulty: str = "Standard") -> Dict[str, Any]:
        """Transitions game state from Exploration to Tactical Combat."""
        self.state = GameState.TACTICAL_COMBAT
        self.active_combat_squad = self.enemies.generate_encounter(difficulty, self.player.active_stratum)
        self.player.current_ap = self.player.max_ap
        log_msg = f"⚔️ ENCOUNTER INITIATED: {len(self.active_combat_squad)} adversaries materialized in {self.player.active_stratum}."
        self.action_log.append(log_msg)
        return self.get_full_game_state()

    def player_attack(self, target_uid: str, action_name: str = "Resonance Strike", attack_spectrum: EnemySpectrum = EnemySpectrum.GOLD) -> Dict[str, Any]:
        """Resolves a player combat attack using 2d6 Arcana rolls and Chromatic Multipliers."""
        if self.state != GameState.TACTICAL_COMBAT:
            return {"error": "Combat action only valid in TACTICAL_COMBAT state."}

        if self.player.current_ap < 2:
            return {"error": "Insufficient AP (Attacks require 2 AP)."}

        target = next((e for e in self.active_combat_squad if e.uid == target_uid and e.is_alive), None)
        if not target:
            return {"error": "Target enemy not found or already defeated."}

        self.player.current_ap -= 2

        # 2d6 Arcana resolution
        arcana_res = self.arcana.resolve_action(action_name, stat_bonus=2)
        total_score = arcana_res["total_score"]
        card = arcana_res["drawn_card"]

        # Calculate Chromatic Multiplier against target
        chroma_mult = self.enemies.calculate_chromatic_multiplier(attack_spectrum, target.spectrum)

        raw_damage = 0
        if total_score >= 10:
            raw_damage = 14
            outcome_str = "CRITICAL RESONANCE"
        elif 7 <= total_score <= 9:
            raw_damage = 9
            outcome_str = "PARTIAL HIT"
            self.player.paradox = min(self.player.max_paradox, self.player.paradox + 1)
        else:
            raw_damage = 4
            outcome_str = "GLANCING STRIKE (Paradox Spike)"
            self.player.paradox = min(self.player.max_paradox, self.player.paradox + 2)

        # Apply Chromatic multiplier & Armor
        modified_dmg = int(raw_damage * chroma_mult)
        effective_damage = max(1, modified_dmg - target.armor)
        target.current_hp = max(0, target.current_hp - effective_damage)

        # Passive check: Rogue Synthete gains AP when damaged
        if "Overclocked_Actuators" in target.passive_trait and target.current_hp > 0:
            target.ap = min(target.max_ap + 2, target.ap + 1)

        mult_desc = f" ({chroma_mult}x Chroma Affinity)" if chroma_mult != 1.0 else ""
        if target.current_hp == 0:
            target.is_alive = False
            self.action_log.append(f"💀 Defeated {target.name}!")

        self.action_log.append(f"Player used {action_name} [{attack_spectrum.value}] on {target.name}: {outcome_str} for {effective_damage} dmg{mult_desc} [Card: {card['name']}]")

        # Inscribe turn into campaign combat log
        self.campaign.record_combat_turn(self.player.character_name, action_name, stat_mod=2)

        # Check for Paradox Break
        if self.player.paradox >= self.player.max_paradox:
            self.trigger_paradox_break()

        # Check for combat victory
        if all(not e.is_alive for e in self.active_combat_squad):
            self.resolve_combat_victory()

        return self.get_full_game_state()

    def end_player_turn(self) -> Dict[str, Any]:
        """Ends the player phase and executes enemy AI behavior tree turns."""
        if self.state != GameState.TACTICAL_COMBAT:
            return {"error": "End turn only available during combat."}

        self.action_log.append("--- Enemy Phase ---")

        for enemy in self.active_combat_squad:
            if not enemy.is_alive:
                continue
            
            ai_actions = self.enemies.decide_ai_turn(
                enemy,
                target_x=self.player.x,
                target_y=self.player.y,
                target_spectrum=self.player.spectrum_affinity,
                player_paradox=self.player.paradox,
                grid_width=self.grid_width,
                grid_height=self.grid_height
            )
            
            for act in ai_actions:
                if act["type"] == "ATTACK":
                    dmg = act["damage"]
                    self.player.current_hp = max(0, self.player.current_hp - dmg)
                    chroma_note = f" ({act.get('chromatic_mult', 1.0)}x Chroma)" if act.get('chromatic_mult', 1.0) != 1.0 else ""
                    self.action_log.append(f"💥 {enemy.name} struck Player with {act['ability']} for {dmg} dmg{chroma_note}!")
                    
                    if act.get("paradox_infliction", 0) > 0:
                        self.player.paradox = min(self.player.max_paradox, self.player.paradox + act["paradox_infliction"])
                    if act.get("luminous_drain", 0.0) > 0:
                        self.action_log.append(f"🌀 {enemy.name} siphoned {int(act['luminous_drain']*100)}% Luminous Probability field!")
                elif act["type"] == "MOVE":
                    self.action_log.append(f"👣 {enemy.name} positioned to ({act['to'][0]}, {act['to'][1]}).")
                elif act["type"] == "ABILITY":
                    self.action_log.append(f"✨ {enemy.name} activated {act['ability']} ({act['effect']}).")
                elif act["type"] == "PARADOX_REACTION":
                    self.action_log.append(f"⚠️ PARADOX REACTION: {act['effect']}")
                    if act.get("damage", 0) > 0:
                        self.player.current_hp = max(0, self.player.current_hp - act["damage"])
                elif act["type"] == "PASSIVE_HEAL":
                    self.action_log.append(f"🌿 {enemy.name}: {act['effect']}")

        # Check player defeat
        if self.player.current_hp <= 0:
            self.state = GameState.SANCTUARY_REST
            self.action_log.append("⚠️ Player defeated! Resonating back at Sanctuary Lithic Rest.")
            self.player.current_hp = self.player.max_hp
            self.player.paradox = 0
            self.active_combat_squad = []
        else:
            # Start new player turn
            self.turn_counter += 1
            self.player.current_ap = self.player.max_ap
            self.action_log.append(f"--- Player Turn {self.turn_counter} (AP Restored to {self.player.max_ap}) ---")

        return self.get_full_game_state()

    def trigger_paradox_break(self):
        """Resolves a 5-point Paradox break event."""
        self.action_log.append("⚡ PARADOX BREAK: Dialetheic buffer collapsed! Permineralizing Harmonic Scar.")
        self.player.paradox = 0
        self.player.emotional_state = "Amethyst/Break"
        self.paraconsistent.process_frame_tick(self.turn_counter, c_pos=0.99, c_neg=0.99)

    def resolve_combat_victory(self):
        """Awards Insight XP, loot materials, and restores exploration state."""
        self.state = GameState.AFTERMATH_LOOT
        self.action_log.append("🏆 VICTORY: Adversary threat extinguished.")
        self.action_log.append("🎁 Rewarded: +150 Insight XP, +3 Permineralized Granite, +1 Lumen Core.")
        self.state = GameState.EXPLORATION
        self.active_combat_squad = []

if __name__ == "__main__":
    game = GameLoopEngine()
    print("[GAME LOOP] Initialized with Adversary Taxonomy and Chromatic Affinities.")
    state = game.start_new_game("Kiri Vespera", "Void Walker")
    print(f"  Player: {state['player']['name']} [{state['player']['spectrum']}] at ({state['player']['x']}, {state['player']['y']})")
    
    print()
    print("[ENCOUNTER] Spawning encounter...")
    state = game.trigger_combat_encounter("Standard")
    for e in state["enemies"]:
        print(f"  - Adversary: {e['name']} [{e['spectrum']}] (HP: {e['hp']}/{e['max_hp']}, Armor: {e['armor']})")

    if state["enemies"]:
        target_uid = state["enemies"][0]["uid"]
        print()
        print(f"[COMBAT] Attacking {target_uid} with Gold Spectrum strike...")
        state = game.player_attack(target_uid, "Lithic Resonator Strike", attack_spectrum=EnemySpectrum.GOLD)
        print(f"  Target HP: {state['enemies'][0]['hp']}/{state['enemies'][0]['max_hp']}")
        print()
        print("[COMBAT] Ending player turn (Triggering Adversary AI Decisions & Chromatic Checks)...")
        state = game.end_player_turn()
        for log in state["action_log"][-4:]:
            print(f"    > {log}")
