"""
Module 3: Bio-Semantic Combat & Somatic Damage Shunts
Implements Layer 11 historical damage accumulation and cryptographic Ash Archive anchoring.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ash_ledger_manager import AshLedgerManager

class SomaticCombatEngine:
    def __init__(self, ledger_path: str = ""):
        self.ash_mgr = AshLedgerManager(ledger_path)

    def apply_somatic_damage(self, entity_state: dict, damage_type: str, raw_damage: float) -> dict:
        rho = entity_state.get("ego_density", 8.3)
        afield = entity_state.get("afield_potency", 0.5)
        archetype = entity_state.get("archetype", "Vanguard")
        spectral = entity_state.get("spectral_constant", "Theta")

        barrier = round(afield * 50.0, 1)
        absorbed = min(barrier, raw_damage)
        penetrating_damage = raw_damage - absorbed
        severity = min(1.0, round(penetrating_damage / 100.0, 2))
        
        if damage_type == "KINETIC_RUPTURE":
            visual_effect = f"Diagonal pauldron shear path (Severity: {severity:.2f}) sealed with gold solder"
            layer11_glyph = "fissure_kinetic_alpha"
        elif damage_type == "COMBUSTION_SLAG":
            visual_effect = f"Thermal soot impregnation and burnt ceramic gradient (Severity: {severity:.2f})"
            layer11_glyph = "soot_radial_burn"
        else:
            visual_effect = f"Surface micro-fracture lattice (Severity: {severity:.2f})"
            layer11_glyph = "lattice_fracture"

        entry = self.ash_mgr.append_historical_scar(
            archetype_id=archetype,
            scar_description=visual_effect,
            severity=severity,
            spectral_constant=spectral
        )

        return {
            "archetype": archetype,
            "raw_damage": raw_damage,
            "barrier_absorbed": absorbed,
            "penetrating_damage": penetrating_damage,
            "layer_11_visual": visual_effect,
            "layer_11_glyph": layer11_glyph,
            "ash_archive_index": entry["index"],
            "j_hash": entry["j_hash"]
        }
