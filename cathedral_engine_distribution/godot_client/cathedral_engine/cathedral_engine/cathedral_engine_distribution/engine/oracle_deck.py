"""
Cathedral-Engine 377-Card Persona Oracle Deck & Interference Engine.
Models the complete 377-card distribution across the 4 Strata Tiers.
"""

from __future__ import annotations
import math
import random
from typing import Dict, List, Tuple, Any, Optional
from .models import OracleCard, Spectral, BelnapValue
from .sanguine_heuristics import SanguineHeuristicsSolver, SanguineResolution
from .database import DatabaseManager

class OracleDeckManager:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.solver = SanguineHeuristicsSolver()
        self.cards: List[OracleCard] = []
        self._initialize_377_deck()

    def _initialize_377_deck(self):
        """Generates and indexes the full 377-Card Persona Oracle distribution."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM oracle_deck_strata")
            count = cursor.fetchone()[0]
            
            if count < 377:
                self.cards = self._generate_377_cards()
                for c in self.cards:
                    cursor.execute("""
                    INSERT OR REPLACE INTO oracle_deck_strata (
                        card_id, name, arcana, tier_strata, spectral,
                        tau_delta, rho_delta, delta_delta, sigma_delta,
                        carrier_freq_hz, flavour_lore
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        c.card_id, c.name, c.arcana, c.tier_strata, c.spectral.value,
                        c.tau_delta, c.rho_delta, c.delta_delta, c.sigma_delta,
                        c.carrier_freq_hz, c.flavour_lore
                    ))
                conn.commit()
            else:
                cursor.execute("SELECT * FROM oracle_deck_strata ORDER BY card_id ASC")
                self.cards = [
                    OracleCard(
                        card_id=row["card_id"],
                        name=row["name"],
                        arcana=row["arcana"],
                        tier_strata=row["tier_strata"],
                        spectral=Spectral(row["spectral"]),
                        tau_delta=row["tau_delta"],
                        rho_delta=row["rho_delta"],
                        delta_delta=row["delta_delta"],
                        sigma_delta=row["sigma_delta"],
                        carrier_freq_hz=row["carrier_freq_hz"],
                        flavour_lore=row["flavour_lore"]
                    )
                    for row in cursor.fetchall()
                ]

    def _generate_377_cards(self) -> List[OracleCard]:
        cards: List[OracleCard] = []
        
        # Archetype templates per Tier
        tier_archetypes = [
            ("Prime Foundations", (1, 94), [
                ("The Tensegrity Architect", "Geometry / Invariants", Spectral.EMERALD, -0.05, -0.08, -0.06, 0.16, "Discontinuous compression struts balanced in pure tensile harmony."),
                ("The Substrate Mason", "Foundations / Bedrock", Spectral.GOLD, -0.08, -0.05, -0.10, 0.18, "Lays cyclopean basalt where emotional law crystallizes."),
                ("The Mortar Sentinel", "Type-Safety / Syntactic Gate", Spectral.TEAL, -0.04, 0.02, -0.08, 0.14, "Computes Consistency Coefficients before allowing data ingress."),
                ("The Rupture Shard", "Trauma / Primary Fracture", Spectral.RED, 0.18, 0.10, 0.15, -0.22, "Where the initial structural breach opened the kinetic forge.")
            ]),
            ("Inner Mandala", (95, 188), [
                ("The Dialetheic Arbiter", "Paraconsistency / Dual Throne", Spectral.GOLD, -0.08, -0.04, -0.15, 0.20, "Judge of the dual-mandate who holds contradiction without collapse."),
                ("The Flesh-Code Cantor", "Biological Resonance / Organon", Spectral.EMERALD, -0.06, -0.06, -0.05, 0.15, "Sings the 1.5 Hz somatic baseline into the mineral matrix."),
                ("The Autopoietic Weaver", "Recursive Loop / Regeneration", Spectral.TEAL, -0.02, 0.04, -0.06, 0.12, "Spins feedback threads into self-repairing sanctuary-flesh."),
                ("The Condenser Siphon", "Reservoir / Thermal Drain", Spectral.BLUE, 0.05, -0.02, 0.04, 0.08, "Stores cryogenic sorrow to cool the 42.0 Hz civic logic furnaces.")
            ]),
            ("Outer Choirs", (189, 282), [
                ("The Arch-Registrar", "Bureaucracy / Choral Catalog", Spectral.TEAL, -0.10, 0.02, -0.12, 0.14, "A cataloger whose quill carves directly into obsidian, stabilizing drift."),
                ("The Iron Liturgist", "Perimeter / Martial Scalpel", Spectral.RED, 0.14, 0.08, 0.12, -0.16, "Wields the Iron Key to excise anomalous narrative pressure."),
                ("The Aether Conductor", "Transit / Geodesic Conduit", Spectral.EMERALD, -0.04, -0.02, -0.05, 0.10, "Routes high-velocity state packets between distant spires."),
                ("The Keystone Fracture", "Catastrophe / Resonant Shear", Spectral.RED, 0.22, 0.12, 0.18, -0.28, "When ten thousand voices scream at the same frequency, basalt shears.")
            ]),
            ("Inner Shadow Canon", (283, 377), [
                ("The Siphon Thief", "Entropic Drain / Shadow Flora", Spectral.VIOLET, 0.06, 0.18, 0.04, -0.10, "Feeds on un-indexed memory vapor leaking from fractured condensers."),
                ("The Necro-Parser", "Dead Logic / Annihilation Ritual", Spectral.BLUE, -0.12, 0.05, -0.10, 0.15, "Retrieves carbonized paradoxes to crash against active logic storms."),
                ("The Null Cartographer", "Obsidian Void / Excision", Spectral.NULL, -0.05, -0.10, 0.08, 0.12, "Maps regions where carrier waves drop to absolute zero."),
                ("The Ash Sovereign Ω", "Master Arcana / Terminal Genesis", Spectral.NULL, -0.25, -0.20, -0.25, 0.35, "The terminal state where all trauma is carbonized into the block universe.")
            ])
        ]

        spectrals_pool = [Spectral.GOLD, Spectral.TEAL, Spectral.BLUE, Spectral.RED, Spectral.VIOLET, Spectral.EMERALD, Spectral.NULL]

        for tier_name, (start_id, end_id), templates in tier_archetypes:
            for card_id in range(start_id, end_id + 1):
                tmpl_idx = (card_id - start_id) % len(templates)
                base_name, base_arcana, base_spec, t_d, r_d, d_d, s_d, base_lore = templates[tmpl_idx]
                
                # Introduce deterministic variation per card index
                seed_factor = math.sin(card_id * 13.37)
                spec = base_spec if (card_id % 3 != 0) else spectrals_pool[card_id % len(spectrals_pool)]
                
                name = f"{base_name} {'I' * ((card_id % 7) + 1)}" if (card_id % len(templates) != 0) else base_name
                arcana = f"{tier_name} / {base_arcana}"
                carrier_hz = 130.81 * (1.0 + 0.05 * (card_id % 12 - 6))
                
                card = OracleCard(
                    card_id=card_id,
                    name=name,
                    arcana=arcana,
                    tier_strata=tier_name,
                    spectral=spec,
                    tau_delta=round(t_d + seed_factor * 0.04, 3),
                    rho_delta=round(r_d + seed_factor * 0.03, 3),
                    delta_delta=round(d_d + seed_factor * 0.03, 3),
                    sigma_delta=round(s_d + seed_factor * 0.05, 3),
                    carrier_freq_hz=round(carrier_hz, 2),
                    flavour_lore=f"{base_lore} (Strata Index #{card_id:03d})"
                )
                cards.append(card)
        return cards

    def draw(
        self,
        spectrum_mode: str = "Gold-Obsidian",
        active_spectrum: Spectral = Spectral.GOLD,
        player_assertion: BelnapValue = BelnapValue.T,
        card_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Draws an Oracle Card and calculates interference patterns against active spectrum.
        """
        if card_id is not None and 1 <= card_id <= 377:
            card = self.cards[card_id - 1]
        else:
            card = random.choice(self.cards)

        # Calculate Spectral Interference Pattern
        # Wave amplitude interference: I = A1^2 + A2^2 + 2*A1*A2*cos(delta_theta)
        phase_map = {
            Spectral.GOLD: 0.0,
            Spectral.TEAL: math.pi / 3,
            Spectral.EMERALD: 2 * math.pi / 3,
            Spectral.BLUE: math.pi,
            Spectral.RED: 4 * math.pi / 3,
            Spectral.VIOLET: 5 * math.pi / 3,
            Spectral.NULL: 0.0
        }
        theta_player = phase_map.get(active_spectrum, 0.0)
        theta_card = phase_map.get(card.spectral, 0.0)
        delta_theta = abs(theta_player - theta_card)
        
        a1 = 1.0
        a2 = 0.8 if spectrum_mode == "Prismatic" else (1.2 if card.spectral in (Spectral.GOLD, Spectral.NULL) else 0.6)
        interference_intensity = round(a1**2 + a2**2 + 2 * a1 * a2 * math.cos(delta_theta), 3)
        
        # Dialetheic Collision Resolution:
        # If card is Red/Violet vs Player assertion True -> simulates adversarial collision
        card_assertion = BelnapValue.T if card.spectral in (Spectral.GOLD, Spectral.TEAL, Spectral.EMERALD) else (
            BelnapValue.F if card.spectral in (Spectral.RED, Spectral.BLUE) else (
                BelnapValue.N if card.spectral == Spectral.NULL else BelnapValue.B
            )
        )
        
        collision_res = self.solver.resolve_collision(
            claim_a=player_assertion,
            claim_b=card_assertion,
            spectral_a=active_spectrum,
            spectral_b=card.spectral,
            entropy_local=0.45
        )

        return {
            "card": card.to_dict(),
            "spectrum_mode": spectrum_mode,
            "active_spectrum": active_spectrum.value,
            "phase_delta_radians": round(delta_theta, 4),
            "interference_intensity": interference_intensity,
            "interference_type": "Constructive" if interference_intensity > 2.0 else ("Destructive" if interference_intensity < 1.0 else "Neutral"),
            "belnap_resolution": {
                "truth_value": collision_res.truth_value.value,
                "is_dialetheia": collision_res.is_dialetheia,
                "harmonic_scar_formed": collision_res.harmonic_scar_formed,
                "algorithmic_cost": collision_res.algorithmic_cost,
                "consistency_coefficient": collision_res.consistency_coefficient,
                "divergence_vector": collision_res.divergence_vector,
                "description": collision_res.description
            },
            "net_telemetry_delta": {
                "tau_delta": round(card.tau_delta + collision_res.telemetry_delta["tau_delta"], 3),
                "rho_delta": round(card.rho_delta + collision_res.telemetry_delta["rho_delta"], 3),
                "delta_delta": round(card.delta_delta + collision_res.telemetry_delta["delta_delta"], 3),
                "sigma_delta": round(card.sigma_delta + collision_res.telemetry_delta["sigma_delta"], 3)
            }
        }
