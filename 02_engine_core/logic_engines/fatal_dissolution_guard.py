"""
Fatal Dissolution Guard Engine
Enforces Master Report Ω-FD-001:
Dissolution = Loss of Boundary + Loss of Lineage + Loss of Recoverability.
Evaluates state metrics against structural identity thresholds to prevent uncontained collapse.
"""

from typing import Dict, Any, List

class FatalDissolutionGuard:
    def __init__(self, i_identity_min: float = 0.5, l_max: float = 1.0, fog_max: int = 2):
        self.i_identity_min = i_identity_min
        self.l_max = l_max
        self.fog_max = fog_max

    def evaluate_dissolution_risk(self, state_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates system metrics against the four terminal questions:
        1. What remains?
        2. What is still connected?
        3. What history survives?
        4. Can a valid successor state still be generated?
        """
        recoverable_info = state_metrics.get("recoverable_information", 1.0)
        identity_mass = state_metrics.get("identity_mass", 1.0)
        pressure = state_metrics.get("pressure", 0.0)
        fog = state_metrics.get("fog", 0)
        lineage_intact = state_metrics.get("lineage_intact", True)

        is_dissolved = (
            recoverable_info < identity_mass or
            pressure > self.l_max * 1.5 or
            fog > self.fog_max or
            not lineage_intact
        )

        status = "FATAL_DISSOLUTION" if is_dissolved else ("STRAIN" if pressure > self.l_max else "STABLE")

        return {
            "status": status,
            "is_dissolved": is_dissolved,
            "metrics": {
                "recoverable_info": recoverable_info,
                "identity_mass": identity_mass,
                "pressure": pressure,
                "fog": fog,
                "lineage_intact": lineage_intact
            }
        }
