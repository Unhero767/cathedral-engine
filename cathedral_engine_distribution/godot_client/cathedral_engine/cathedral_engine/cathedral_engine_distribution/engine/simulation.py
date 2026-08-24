"""
Cathedral-Engine Persona Oracle & Belnap Solver Simulation Harness.
Executes multi-turn automated playtest simulations across 3,000+ state transitions.
"""

from __future__ import annotations
import math
import random
import time
from typing import Dict, List, Any
from .models import BelnapValue, Spectral
from .database import DatabaseManager
from .oracle_deck import OracleDeckManager

class PlaytestSimulationRunner:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.oracle = OracleDeckManager(db)

    def run_simulation(self, total_turns: int = 3000) -> Dict[str, Any]:
        """
        Executes an automated multi-turn playtest simulation.
        Monitors pattern distributions, dialetheic collisions, and stability.
        """
        t0 = time.time()
        
        # State metrics
        tau_pol = 0.44
        rho_res = 0.38
        delta_fac = 0.35
        sigma_coh = 0.72
        
        belnap_counts = {"T": 0, "F": 0, "B": 0, "N": 0}
        spectral_counts = {s.value: 0 for s in Spectral}
        interference_counts = {"Constructive": 0, "Destructive": 0, "Neutral": 0}
        harmonic_scars_created = 0
        total_algorithmic_cost = 0.0
        
        lyapunov_history: List[float] = []
        spectrum_modes = ["Gold-Obsidian", "Prismatic"]
        player_spectrals = [Spectral.GOLD, Spectral.TEAL, Spectral.EMERALD, Spectral.BLUE, Spectral.RED, Spectral.VIOLET, Spectral.NULL]

        for turn in range(1, total_turns + 1):
            active_spec = random.choice(player_spectrals)
            mode = random.choice(spectrum_modes)
            p_assert = random.choice([BelnapValue.T, BelnapValue.F, BelnapValue.B, BelnapValue.N])
            
            draw_res = self.oracle.draw(
                spectrum_mode=mode,
                active_spectrum=active_spec,
                player_assertion=p_assert
            )
            
            # Record counts
            bv = draw_res["belnap_resolution"]["truth_value"]
            belnap_counts[bv] = belnap_counts.get(bv, 0) + 1
            
            card_spec = draw_res["card"]["spectral"]
            spectral_counts[card_spec] = spectral_counts.get(card_spec, 0) + 1
            
            itype = draw_res["interference_type"]
            interference_counts[itype] = interference_counts.get(itype, 0) + 1
            
            if draw_res["belnap_resolution"]["harmonic_scar_formed"]:
                harmonic_scars_created += 1
                
            total_algorithmic_cost += draw_res["belnap_resolution"]["algorithmic_cost"]
            
            # Apply deltas
            deltas = draw_res["net_telemetry_delta"]
            tau_pol = max(0.0, min(1.0, tau_pol + deltas["tau_delta"] * 0.1))
            rho_res = max(0.0, min(1.0, rho_res + deltas["rho_delta"] * 0.1))
            delta_fac = max(0.0, min(1.0, delta_fac + deltas["delta_delta"] * 0.1))
            sigma_coh = max(0.0, min(1.0, sigma_coh + deltas["sigma_delta"] * 0.1))
            
            # Compute instantaneous Lyapunov metric λ = ln(|δV(t)|)
            v_norm = math.sqrt(tau_pol**2 + rho_res**2 + delta_fac**2 + (1.0 - sigma_coh)**2)
            lyapunov_history.append(math.log(max(1e-5, v_norm)))

        elapsed = time.time() - t0
        avg_cost = total_algorithmic_cost / total_turns
        avg_lyapunov = sum(lyapunov_history) / len(lyapunov_history)
        
        # Log to ash_ledger
        summary_payload = {
            "total_turns": total_turns,
            "elapsed_seconds": round(elapsed, 3),
            "belnap_distribution": belnap_counts,
            "spectral_distribution": spectral_counts,
            "interference_distribution": interference_counts,
            "harmonic_scars_created": harmonic_scars_created,
            "average_algorithmic_cost": round(avg_cost, 4),
            "average_lyapunov_exponent": round(avg_lyapunov, 4),
            "final_state": {
                "tau_pol": round(tau_pol, 3),
                "rho_res": round(rho_res, 3),
                "delta_fac": round(delta_fac, 3),
                "sigma_coh": round(sigma_coh, 3)
            }
        }
        
        block = self.db.append_ash_block(event_type="ORACLE_PLAYTEST_SIMULATION", payload=summary_payload)
        summary_payload["ash_block_hash"] = block.block_hash
        summary_payload["ash_block_index"] = block.index

        return summary_payload
