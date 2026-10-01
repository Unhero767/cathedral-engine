# ==============================================================================
# SPECTRAL COMBAT MATRIX & DEFENSE MITIGATION ENGINE
# ==============================================================================

SPECTRAL_AFFINITY_MATRIX = {
    "Gold": {
        "Gold": 1.0,
        "Teal": 1.25,
        "Blue": 1.5,
        "Red": 0.75,
        "Violet": 1.5,
        "Emerald": 1.0,
        "Bronze-Obsidian": 0.5,
        "Obsidian": 0.5
    },
    "Teal": {
        "Gold": 0.75,
        "Teal": 1.0,
        "Blue": 1.25,
        "Red": 1.5,
        "Violet": 0.75,
        "Emerald": 1.5,
        "Bronze-Obsidian": 0.5,
        "Obsidian": 0.5
    },
    "Blue": {
        "Gold": 0.5,
        "Teal": 1.5,
        "Blue": 1.0,
        "Red": 1.25,
        "Violet": 1.0,
        "Emerald": 0.75,
        "Bronze-Obsidian": 1.5,
        "Obsidian": 1.5
    },
    "Red": {
        "Gold": 1.25,
        "Teal": 0.5,
        "Blue": 1.5,
        "Red": 1.0,
        "Violet": 1.25,
        "Emerald": 0.5,
        "Bronze-Obsidian": 1.0,
        "Obsidian": 1.0
    },
    "Violet": {
        "Gold": 0.5,
        "Teal": 1.5,
        "Blue": 1.0,
        "Red": 0.75,
        "Violet": 1.0,
        "Emerald": 1.5,
        "Bronze-Obsidian": 1.25,
        "Obsidian": 1.25
    },
    "Emerald": {
        "Gold": 1.5,
        "Teal": 0.75,
        "Blue": 1.25,
        "Red": 1.5,
        "Violet": 0.5,
        "Emerald": 1.0,
        "Bronze-Obsidian": 1.0,
        "Obsidian": 1.0
    },
    "Bronze-Obsidian": {
        "Gold": 1.0,
        "Teal": 1.0,
        "Blue": 0.5,
        "Red": 1.0,
        "Violet": 0.75,
        "Emerald": 1.0,
        "Bronze-Obsidian": 0.0,
        "Obsidian": 0.0
    },
    "Obsidian": {
        "Gold": 1.0,
        "Teal": 1.0,
        "Blue": 0.5,
        "Red": 1.0,
        "Violet": 0.75,
        "Emerald": 1.0,
        "Bronze-Obsidian": 0.0,
        "Obsidian": 0.0
    }
}

BASE_DEFENSE_REDUCTION_COEFF = 0.04
MIN_DAMAGE_FLOOR = 1
CARRIER_RESONANCE_BONUS = 1.20
PARADOX_STRAIN_RETALIATION_RATE = 0.10

def compute_mitigated_damage(base_potency, attacker_spectrum, defender_spectrum, defender_defense, is_carrier_aligned=False, strain_mod=1.0):
    affinity_mult = SPECTRAL_AFFINITY_MATRIX.get(attacker_spectrum, {}).get(defender_spectrum, 1.0)
    mitigation_factor = 1.0 / (1.0 + (max(0, defender_defense) * BASE_DEFENSE_REDUCTION_COEFF))
    carrier_mult = CARRIER_RESONANCE_BONUS if is_carrier_aligned else 1.0
    raw_power = base_potency * affinity_mult * carrier_mult * strain_mod
    net_dmg = max(MIN_DAMAGE_FLOOR, int(round(raw_power * mitigation_factor)))
    return {
        "net_damage": net_dmg,
        "affinity_multiplier": affinity_mult,
        "mitigation_percentage": round((1.0 - mitigation_factor) * 100, 2),
        "is_critical": affinity_mult >= 1.5
    }
