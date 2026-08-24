"""
Cathedral-Engine Multi-Agent Belnap-Dunn Dialetheic Wargaming Engine (N >= 4).
Simulates multi-agent adversarial battles between the 4 Choirs:
1. Choir Alpha (Iron Liturgy - Red / True)
2. Choir Beta (Aether Transit - Emerald / False)
3. Choir Gamma (Dialetheic Core - Gold / Both)
4. Shadow Enclave (Obsidian - Null / Neither)
"""

from __future__ import annotations
import math
import random
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Any

from .models import Spectral, BelnapValue
from .sanguine_heuristics import SanguineHeuristicsSolver, SanguineResolution
from .database import DatabaseManager

@dataclass
class FactionAgent:
    faction_id: str
    name: str
    spectral: Spectral
    intent: str
    assertion: BelnapValue
    strength: float = 1.0
    coherence: float = 0.85

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["spectral"] = self.spectral.value
        d["assertion"] = self.assertion.value
        return d

class DialetheicWargameEngine:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.solver = SanguineHeuristicsSolver()

    def get_canonical_factions(self) -> List[FactionAgent]:
        return [
            FactionAgent(
                faction_id="choir_alpha",
                name="Choir Alpha (Iron Liturgy)",
                spectral=Spectral.RED,
                intent="Total Perimeter Fortification & Gate Lockout",
                assertion=BelnapValue.T,
                strength=1.2,
                coherence=0.88
            ),
            FactionAgent(
                faction_id="choir_beta",
                name="Choir Beta (Aether Transit)",
                spectral=Spectral.EMERALD,
                intent="Continuous Gate Dilation & Memory Flow",
                assertion=BelnapValue.F,
                strength=1.0,
                coherence=0.82
            ),
            FactionAgent(
                faction_id="choir_gamma",
                name="Choir Gamma (Dialetheic Core)",
                spectral=Spectral.GOLD,
                intent="Superpositional A-Field Shielding",
                assertion=BelnapValue.B,
                strength=1.4,
                coherence=0.95
            ),
            FactionAgent(
                faction_id="shadow_enclave",
                name="Shadow Enclave (Obsidian)",
                spectral=Spectral.NULL,
                intent="Un-Indexed Ash Siphon Extraction",
                assertion=BelnapValue.N,
                strength=0.9,
                coherence=0.70
            ),
        ]

    def run_wargame(self, rounds: int = 4) -> Dict[str, Any]:
        """
        Executes an N=4 paraconsistent wargame across multiple tactical rounds.
        """
        factions = self.get_canonical_factions()
        round_logs: List[Dict[str, Any]] = []
        
        # State tracking
        tau_pol = 0.50
        rho_res = 0.45
        delta_fac = 0.40
        sigma_coh = 0.70
        total_scars = 0

        for r_num in range(1, rounds + 1):
            # Dynamic tactical assertions per round
            if r_num == 2:
                factions[0].assertion = BelnapValue.B # Alpha adapts to contradiction
                factions[3].assertion = BelnapValue.F # Shadow strikes
            elif r_num == 3:
                factions[1].assertion = BelnapValue.T # Beta counter-asserts
                factions[2].assertion = BelnapValue.B # Gamma maintains superposition
            elif r_num == 4:
                factions[0].assertion = BelnapValue.T
                factions[1].assertion = BelnapValue.F
                factions[2].assertion = BelnapValue.B
                factions[3].assertion = BelnapValue.N

            # Global Bilattice Join across all 4 agents
            global_join = factions[0].assertion
            for f in factions[1:]:
                global_join = BelnapValue.join(global_join, f.assertion)

            # Pairwise clash between antagonistic poles: Alpha (Red) vs Beta (Emerald)
            clash_res = self.solver.resolve_collision(
                claim_a=factions[0].assertion,
                claim_b=factions[1].assertion,
                spectral_a=factions[0].spectral,
                spectral_b=factions[1].spectral,
                entropy_local=0.48 + 0.05 * r_num
            )

            if clash_res.harmonic_scar_formed:
                total_scars += 1

            # Telemetry impact
            tau_pol = max(0.0, min(1.0, tau_pol + clash_res.telemetry_delta["tau_delta"]))
            rho_res = max(0.0, min(1.0, rho_res + clash_res.telemetry_delta["rho_delta"]))
            delta_fac = max(0.0, min(1.0, delta_fac + clash_res.telemetry_delta["delta_delta"]))
            sigma_coh = max(0.0, min(1.0, sigma_coh + clash_res.telemetry_delta["sigma_delta"]))

            round_entry = {
                "round": r_num,
                "factions": [f.to_dict() for f in factions],
                "global_bilattice_join": global_join.value,
                "primary_clash": {
                    "combatants": f"{factions[0].name} vs {factions[1].name}",
                    "resolution": clash_res.truth_value.value,
                    "harmonic_scar": clash_res.harmonic_scar_formed,
                    "algorithmic_cost": clash_res.algorithmic_cost,
                    "consistency_c_tau": clash_res.consistency_coefficient,
                    "description": clash_res.description
                },
                "state_after": {
                    "tau_pol": round(tau_pol, 3),
                    "rho_res": round(rho_res, 3),
                    "delta_fac": round(delta_fac, 3),
                    "sigma_coh": round(sigma_coh, 3)
                }
            }
            round_logs.append(round_entry)

        # Commit battle log to Ash Archive
        battle_summary = {
            "rounds_executed": rounds,
            "factions_count": len(factions),
            "final_bilattice_state": round_logs[-1]["global_bilattice_join"],
            "total_harmonic_scars": total_scars,
            "final_state": round_logs[-1]["state_after"],
            "rounds": round_logs
        }
        ash_block = self.db.append_ash_block(event_type="MULTI_AGENT_WARGAME", payload=battle_summary)
        battle_summary["ash_block_hash"] = ash_block.block_hash
        battle_summary["ash_block_index"] = ash_block.index

        return battle_summary
