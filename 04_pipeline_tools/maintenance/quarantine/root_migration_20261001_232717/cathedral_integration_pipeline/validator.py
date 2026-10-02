"""
MLAOS Metalogical Type-Checker and Schema Validator
"""
import json, os
from typing import Dict, Any, Tuple, List

CANONICAL_SPECTRAL_CONSTANTS = {
    "Theta": {"color": "#D4AF37", "wavelength_nm": 585, "semantic": "Joy / Law"},
    "Psi": {"color": "#008080", "wavelength_nm": 490, "semantic": "Curiosity / Logic"},
    "Delta": {"color": "#002147", "wavelength_nm": 440, "semantic": "Sorrow / Archive"},
    "Phi": {"color": "#8B0000", "wavelength_nm": 680, "semantic": "Anger / Remaking"},
    "Omega": {"color": "#301934", "wavelength_nm": 405, "semantic": "Fear / Shadow"},
    "Epsilon": {"color": "#50C878", "wavelength_nm": 520, "semantic": "Love / Healing"},
    "Null": {"color": "#121212", "wavelength_nm": 0, "semantic": "Void / Anti-Resonance"}
}

REQUIRED_RECIPE_FIELDS = ["archetype", "spectral_constant", "ego_density", "afield_potency"]

class MLAOSValidator:
    def validate_character_recipe(self, recipe: Dict[str, Any]) -> Tuple[bool, List[str], float]:
        errors = []
        for field in REQUIRED_RECIPE_FIELDS:
            if field not in recipe:
                errors.append(f"Missing required field: '{field}'")

        if errors:
            return False, errors, 0.0

        spec = recipe.get("spectral_constant")
        if spec not in CANONICAL_SPECTRAL_CONSTANTS:
            errors.append(f"Invalid spectral_constant '{spec}'.")

        rho = recipe.get("ego_density", 0.0)
        if not isinstance(rho, (int, float)) or rho <= 0.0 or rho > 20.0:
            errors.append(f"Ego density (rho) out of bounds: {rho}.")

        afield = recipe.get("afield_potency", 0.0)
        if not isinstance(afield, (int, float)) or afield < 0.0 or afield > 2.0:
            errors.append(f"A-Field potency out of bounds: {afield}.")

        delta_rho = abs(rho - 8.3)
        epsilon_local = 1.0 + (delta_rho * 0.15)
        w_a = float(afield) * 1.5
        c_tau = round(w_a / epsilon_local, 4)

        return len(errors) == 0, errors, c_tau
