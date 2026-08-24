import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Tuple, Optional

class EnemySpectrum(str, Enum):
    GOLD = "Gold"
    OBSIDIAN = "Obsidian"
    CRIMSON = "Crimson"
    SAPPHIRE = "Sapphire"
    AMETHYST = "Amethyst"
    TEAL = "Teal"
    EMERALD = "Emerald"

# --- 7-SPECTRUM CHROMATIC MATRIX (Weaknesses & Resistances) ---
CHROMATIC_MATRIX = {
    EnemySpectrum.GOLD: {"weak_to": EnemySpectrum.CRIMSON, "resists": EnemySpectrum.OBSIDIAN},
    EnemySpectrum.OBSIDIAN: {"weak_to": EnemySpectrum.GOLD, "resists": EnemySpectrum.SAPPHIRE},
    EnemySpectrum.CRIMSON: {"weak_to": EnemySpectrum.SAPPHIRE, "resists": EnemySpectrum.GOLD},
    EnemySpectrum.SAPPHIRE: {"weak_to": EnemySpectrum.AMETHYST, "resists": EnemySpectrum.CRIMSON},
    EnemySpectrum.AMETHYST: {"weak_to": EnemySpectrum.TEAL, "resists": EnemySpectrum.SAPPHIRE},
    EnemySpectrum.TEAL: {"weak_to": EnemySpectrum.EMERALD, "resists": EnemySpectrum.AMETHYST},
    EnemySpectrum.EMERALD: {"weak_to": EnemySpectrum.OBSIDIAN, "resists": EnemySpectrum.TEAL}
}

@dataclass
class EnemyAbility:
    name: str
    ap_cost: int
    base_damage: int
    range_tiles: int
    spectrum: EnemySpectrum
    is_ranged: bool = False
    paradox_infliction: int = 0
    luminous_drain_pct: float = 0.0
    status_effect: Optional[str] = None
    description: str = ""

@dataclass
class EnemyInstance:
    uid: str
    archetype: str
    name: str
    spectrum: EnemySpectrum
    max_hp: int
    current_hp: int
    armor: int
    x: int
    y: int
    ap: int
    max_ap: int
    mobility_tiles: int
    abilities: List[EnemyAbility]
    passive_trait: str
    can_phase_through_walls: bool = False
    ai_type: str = "Aggressive"
    is_overdriven: bool = False
    is_petrified: bool = False
    is_alive: bool = True

class EnemyEngine:
    """
    Cathedral-Engine Advanced Adversary & Tactical AI System
    Manages Adversary Taxonomy, Chromatic Affinity Calculations,
    Distance Checks (Melee vs Ranged), and Paradox Break Threshold Reactions.
    """
    def __init__(self):
        self.archetypes = self._init_archetypes()

    def calculate_chromatic_multiplier(self, attack_spectrum: EnemySpectrum, target_spectrum: EnemySpectrum) -> float:
        """Computes damage multiplier based on chromatic affinities."""
        matrix = CHROMATIC_MATRIX.get(target_spectrum, {})
        if matrix.get("weak_to") == attack_spectrum:
            return 1.5  # Critical Chromatic Weakness
        elif matrix.get("resists") == attack_spectrum:
            return 0.5  # Chromatic Resistance
        return 1.0     # Standard Affinity

    def _init_archetypes(self) -> Dict[str, Dict[str, Any]]:
        return {
            "LITHIC_SENTINEL": {
                "name": "Lithic Sentinel",
                "spectrum": EnemySpectrum.GOLD,
                "hp": 45,
                "armor": 4,
                "max_ap": 3,
                "mobility_tiles": 1,
                "can_phase": False,
                "passive": "Permineralized_Carapace (Takes 50% reduced kinetic pushback)",
                "ai_type": "Tank_Anchor",
                "abilities": [
                    EnemyAbility("Ground Slam", ap_cost=2, base_damage=10, range_tiles=1, spectrum=EnemySpectrum.GOLD, is_ranged=False, description="Crushes adjacent stone tiles with monumental torque."),
                    EnemyAbility("Lithic Bulwark", ap_cost=1, base_damage=0, range_tiles=0, spectrum=EnemySpectrum.GOLD, status_effect="Armor_Up", description="Reinforces granite outer layer (+3 Armor)."),
                    EnemyAbility("Seismic Wave", ap_cost=2, base_damage=7, range_tiles=2, spectrum=EnemySpectrum.GOLD, is_ranged=True, description="Radiates seismic shockwave along floor strata.")
                ]
            },
            "VOID_SHADE": {
                "name": "Asema Void Shade",
                "spectrum": EnemySpectrum.OBSIDIAN,
                "hp": 22,
                "armor": 0,
                "max_ap": 4,
                "mobility_tiles": 3,
                "can_phase": True,
                "passive": "Phase_Shift (Phases through monoliths and physical boundaries)",
                "ai_type": "Phase_Kiter",
                "abilities": [
                    EnemyAbility("Shadow Cleave", ap_cost=2, base_damage=12, range_tiles=1, spectrum=EnemySpectrum.OBSIDIAN, is_ranged=False, paradox_infliction=1, description="Slices through somatic heat sinks, ignoring target armor."),
                    EnemyAbility("Luminous Drain", ap_cost=2, base_damage=6, range_tiles=3, spectrum=EnemySpectrum.OBSIDIAN, is_ranged=True, paradox_infliction=2, luminous_drain_pct=0.15, description="Siphons player probability field and restores 6 HP to shade."),
                    EnemyAbility("Dialetheic Burst", ap_cost=3, base_damage=20, range_tiles=2, spectrum=EnemySpectrum.OBSIDIAN, is_ranged=True, description="Self-destructs in a localized logic storm when Paradox >= 5.")
                ]
            },
            "ROGUE_SYNTHETE": {
                "name": "Rogue Synthete",
                "spectrum": EnemySpectrum.CRIMSON,
                "hp": 28,
                "armor": 1,
                "max_ap": 5,
                "mobility_tiles": 2,
                "can_phase": False,
                "passive": "Overclocked_Actuators (+1 AP when taking damage)",
                "ai_type": "Flanker_Overdriver",
                "abilities": [
                    EnemyAbility("Monoblade Flurry", ap_cost=2, base_damage=8, range_tiles=1, spectrum=EnemySpectrum.CRIMSON, is_ranged=False, description="High-frequency dual ceramic blade strikes."),
                    EnemyAbility("Paradox Overload", ap_cost=2, base_damage=7, range_tiles=2, spectrum=EnemySpectrum.CRIMSON, is_ranged=True, paradox_infliction=2, description="Forces destructive dialectic feedback into player buffer."),
                    EnemyAbility("Phase Flip", ap_cost=1, base_damage=0, range_tiles=2, spectrum=EnemySpectrum.CRIMSON, status_effect="Reposition", description="Instantly shifts 2 tiles to establish flanking vector.")
                ]
            },
            "CHOIR_SIREN": {
                "name": "Choir Siren",
                "spectrum": EnemySpectrum.SAPPHIRE,
                "hp": 20,
                "armor": 0,
                "max_ap": 3,
                "mobility_tiles": 2,
                "can_phase": False,
                "passive": "Resonance_Dampener (Reduces player AP generation by 1)",
                "ai_type": "Ranged_Disruptor",
                "abilities": [
                    EnemyAbility("Resonance Wail", ap_cost=2, base_damage=7, range_tiles=4, spectrum=EnemySpectrum.SAPPHIRE, is_ranged=True, paradox_infliction=1, description="Acoustic pressure targeting neural threading."),
                    EnemyAbility("Somatic Disruption", ap_cost=1, base_damage=0, range_tiles=3, spectrum=EnemySpectrum.SAPPHIRE, is_ranged=True, status_effect="Slow", description="Overheats player heat sink, reducing AP.")
                ]
            },
            "AUTOPOIETIC_CHIMERA": {
                "name": "Autopoietic Chimera",
                "spectrum": EnemySpectrum.EMERALD,
                "hp": 34,
                "armor": 2,
                "max_ap": 4,
                "mobility_tiles": 2,
                "can_phase": False,
                "passive": "Cellular_Permineralization (Regenerates 5 HP at start of each round)",
                "ai_type": "Brawler_Regenerator",
                "abilities": [
                    EnemyAbility("Tensegrity Strike", ap_cost=2, base_damage=9, range_tiles=1, spectrum=EnemySpectrum.EMERALD, is_ranged=False, description="Biomechanical arch strike."),
                    EnemyAbility("Autopoietic Surge", ap_cost=1, base_damage=0, range_tiles=0, spectrum=EnemySpectrum.EMERALD, status_effect="Heal_Self", description="Regenerates 8 HP and clears status debuffs.")
                ]
            }
        }

    def spawn_enemy(self, archetype_key: str, uid: str, x: int, y: int) -> EnemyInstance:
        """Spawns an enemy instance from archetype template."""
        arch = self.archetypes.get(archetype_key, self.archetypes["LITHIC_SENTINEL"])
        return EnemyInstance(
            uid=uid,
            archetype=archetype_key,
            name=arch["name"],
            spectrum=arch["spectrum"],
            max_hp=arch["hp"],
            current_hp=arch["hp"],
            armor=arch["armor"],
            x=x,
            y=y,
            ap=arch["max_ap"],
            max_ap=arch["max_ap"],
            mobility_tiles=arch["mobility_tiles"],
            abilities=[EnemyAbility(**ab.__dict__) for ab in arch["abilities"]],
            passive_trait=arch["passive"],
            can_phase_through_walls=arch["can_phase"],
            ai_type=arch["ai_type"]
        )

    def generate_encounter(self, difficulty: str = "Standard", chamber_stratum: str = "Prime Foundations") -> List[EnemyInstance]:
        """Generates thematic enemy squads tailored to structural strata."""
        squad = []
        if chamber_stratum == "Prime Foundations":
            squad.append(self.spawn_enemy("LITHIC_SENTINEL", "enemy_sentinel_01", 5, 2))
            squad.append(self.spawn_enemy("CHOIR_SIREN", "enemy_siren_01", 6, 5))
        elif chamber_stratum == "Shadow Canon":
            squad.append(self.spawn_enemy("VOID_SHADE", "enemy_shade_01", 5, 2))
            squad.append(self.spawn_enemy("VOID_SHADE", "enemy_shade_02", 6, 4))
            squad.append(self.spawn_enemy("ROGUE_SYNTHETE", "enemy_synthete_01", 4, 6))
        else:
            squad.append(self.spawn_enemy("ROGUE_SYNTHETE", "enemy_synthete_01", 5, 3))
            squad.append(self.spawn_enemy("AUTOPOIETIC_CHIMERA", "enemy_chimera_01", 6, 2))
        return squad

    def decide_ai_turn(
        self,
        enemy: EnemyInstance,
        target_x: int,
        target_y: int,
        target_spectrum: EnemySpectrum = EnemySpectrum.TEAL,
        player_paradox: int = 0,
        grid_width: int = 8,
        grid_height: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Adversary AI Decision Tree:
        1. Evaluates Paradox Threshold Reactions (Self-destruct, Overdrive, or Petrified Stasis).
        2. Performs Distance Checks (Melee vs Ranged positioning).
        3. Evaluates Chromatic Weaknesses/Resistances to choose optimal ability.
        4. Executes Movement + Ability sequencing.
        """
        actions = []
        enemy.ap = enemy.max_ap

        # Check Passive Regeneration
        if "Cellular_Permineralization" in enemy.passive_trait and enemy.current_hp < enemy.max_hp:
            heal_amt = min(5, enemy.max_hp - enemy.current_hp)
            enemy.current_hp += heal_amt
            actions.append({"type": "PASSIVE_HEAL", "effect": f"Regenerated {heal_amt} HP ({enemy.current_hp}/{enemy.max_hp})"})

        # --- 1. PARADOX THRESHOLD REACTIONS (Triggered when Paradox >= 5) ---
        if player_paradox >= 5 or enemy.is_overdriven:
            if enemy.archetype == "VOID_SHADE":
                dist = abs(enemy.x - target_x) + abs(enemy.y - target_y)
                if dist <= 2:
                    # Self-destruct in Dialetheic Burst
                    enemy.current_hp = 0
                    enemy.is_alive = False
                    actions.append({
                        "type": "PARADOX_REACTION",
                        "reaction": "DIALETHEIC_SELF_DESTRUCT",
                        "damage": 20,
                        "effect": "Asema Void Shade collapsed dialectic buffer in a 20-damage cataclysmic burst!",
                        "remaining_ap": 0
                    })
                    return actions
            elif enemy.archetype == "ROGUE_SYNTHETE" and not enemy.is_overdriven:
                enemy.is_overdriven = True
                enemy.ap += 2
                actions.append({
                    "type": "PARADOX_REACTION",
                    "reaction": "OVERCLOCK_PHASE_FLIP",
                    "effect": "Rogue Synthete entered Overdrive! (+2 AP, +4 Damage on Flurry)",
                    "remaining_ap": enemy.ap
                })
            elif enemy.archetype == "LITHIC_SENTINEL" and not enemy.is_petrified:
                enemy.is_petrified = True
                enemy.armor += 4
                actions.append({
                    "type": "PARADOX_REACTION",
                    "reaction": "PETRIFIED_LOCKDOWN",
                    "effect": "Lithic Sentinel hardened into impenetrable stasis (+4 Armor, reflecting kinetic stress).",
                    "remaining_ap": enemy.ap
                })

        # --- 2. TACTICAL COMBAT & DISTANCE EVALUATION ---
        while enemy.ap > 0 and enemy.is_alive:
            dist = abs(enemy.x - target_x) + abs(enemy.y - target_y)

            # Find all usable attack abilities
            usable_attacks = [
                ab for ab in enemy.abilities 
                if ab.ap_cost <= enemy.ap and ab.base_damage > 0 and dist <= ab.range_tiles
            ]

            # Find self-healing or defensive buffs
            heal_abilities = [
                ab for ab in enemy.abilities 
                if ab.ap_cost <= enemy.ap and ab.status_effect == "Heal_Self" and enemy.current_hp <= (enemy.max_hp * 0.5)
            ]
            buff_abilities = [
                ab for ab in enemy.abilities 
                if ab.ap_cost <= enemy.ap and ab.status_effect == "Armor_Up" and enemy.armor < 6
            ]

            if heal_abilities:
                ab = heal_abilities[0]
                enemy.current_hp = min(enemy.max_hp, enemy.current_hp + 8)
                enemy.ap -= ab.ap_cost
                actions.append({
                    "type": "ABILITY",
                    "ability": ab.name,
                    "effect": f"Healed 8 HP ({enemy.current_hp}/{enemy.max_hp})",
                    "remaining_ap": enemy.ap
                })
            elif buff_abilities and dist > 1:
                ab = buff_abilities[0]
                enemy.armor += 3
                enemy.ap -= ab.ap_cost
                actions.append({
                    "type": "ABILITY",
                    "ability": ab.name,
                    "effect": f"Armor boosted to {enemy.armor}",
                    "remaining_ap": enemy.ap
                })
            elif usable_attacks:
                # Rank attacks by chromatic effectiveness against target
                best_attack = None
                best_effective_dmg = -1

                for ab in usable_attacks:
                    chroma_mult = self.calculate_chromatic_multiplier(ab.spectrum, target_spectrum)
                    overdrive_bonus = 4 if enemy.is_overdriven else 0
                    effective_dmg = (ab.base_damage + overdrive_bonus) * chroma_mult
                    if effective_dmg > best_effective_dmg:
                        best_effective_dmg = effective_dmg
                        best_attack = ab

                enemy.ap -= best_attack.ap_cost
                chroma_mult = self.calculate_chromatic_multiplier(best_attack.spectrum, target_spectrum)
                final_dmg = int((best_attack.base_damage + (4 if enemy.is_overdriven else 0)) * chroma_mult)

                actions.append({
                    "type": "ATTACK",
                    "ability": best_attack.name,
                    "spectrum": best_attack.spectrum.value,
                    "is_ranged": best_attack.is_ranged,
                    "damage": final_dmg,
                    "chromatic_mult": chroma_mult,
                    "paradox_infliction": best_attack.paradox_infliction,
                    "luminous_drain": best_attack.luminous_drain_pct,
                    "target": "Player",
                    "remaining_ap": enemy.ap
                })
            elif enemy.ap >= 1:
                # Tactical Positioning & Distance Check
                wants_to_close = enemy.ai_type in ("Tank_Anchor", "Flanker_Overdriver", "Brawler_Regenerator") or dist > 3
                wants_to_retreat = enemy.ai_type in ("Phase_Kiter", "Ranged_Disruptor") and dist <= 1

                if wants_to_retreat:
                    dx = -1 if target_x > enemy.x else (1 if target_x < enemy.x else 0)
                    dy = -1 if target_y > enemy.y else (1 if target_y < enemy.y else 0)
                elif wants_to_close and dist > 1:
                    dx = 1 if target_x > enemy.x else (-1 if target_x < enemy.x else 0)
                    dy = 1 if target_y > enemy.y else (-1 if target_y < enemy.y else 0)
                else:
                    break

                if abs(target_x - enemy.x) >= abs(target_y - enemy.y) and dx != 0:
                    new_x = max(0, min(grid_width - 1, enemy.x + dx))
                    new_y = enemy.y
                else:
                    new_x = enemy.x
                    new_y = max(0, min(grid_height - 1, enemy.y + dy))

                enemy.x, enemy.y = new_x, new_y
                enemy.ap -= 1
                actions.append({"type": "MOVE", "to": [enemy.x, enemy.y], "remaining_ap": enemy.ap})
            else:
                break

        return actions

if __name__ == "__main__":
    engine = EnemyEngine()
    print("[ENEMY ENGINE] Initialized with 7-Spectrum Chromatic Matrix.")
    print("Chromatic Multiplier (Gold vs Obsidian):", engine.calculate_chromatic_multiplier(EnemySpectrum.GOLD, EnemySpectrum.OBSIDIAN))
    print("Chromatic Multiplier (Crimson vs Gold):", engine.calculate_chromatic_multiplier(EnemySpectrum.CRIMSON, EnemySpectrum.GOLD))
    
    squad = engine.generate_encounter("Standard", "Shadow Canon")
    print()
    print("--- Shadow Canon Squad ---")
    for e in squad:
        print(f"  - {e.name} [{e.spectrum.value}] (HP: {e.current_hp}/{e.max_hp}, Armor: {e.armor}, AP: {e.max_ap}) | Passive: {e.passive_trait}")
    
    print()
    print("[AI SIMULATION] Simulating Asema Void Shade Turn (Player Paradox = 5, Range = 2)...")
    shade = squad[0]
    turns = engine.decide_ai_turn(shade, target_x=4, target_y=2, target_spectrum=EnemySpectrum.GOLD, player_paradox=5)
    for t in turns:
        print(f"  > AI Action: {t}")
