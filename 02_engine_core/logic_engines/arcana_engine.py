import random
import json
import os
from typing import Dict, Any, List, Tuple, Optional

FLUX_MAJORS = [
    "The Axis", "The Threshold", "The Mirror", "The Anvil", 
    "The Prism", "The Void Core", "The Echo Tide"
]

CHROMAS = ["Gold", "Sapphire", "Amethyst", "Crimson", "Teal", "Obsidian", "Rose"]
IDENTITY_VECTORS = ["Sovereign", "Architect", "Valkyrie", "Nomad", "Cipher", "Warden", "Drifter"]

REBELLION_CARDS = [
    "Plasma Phase-Flip", "Structural Shear", "Axiom Fracture", "Void Inversion",
    "Resonance Spike", "Lithic Rebirth", "Recursive Echo", "Entropy Reversal",
    "Boundary Dissolution", "Phase Lock", "Vector Reversal", "Thermal Squeeze",
    "Kinetic Surge", "Prismatic Shift", "Core Meltdown", "Shadow Cleave",
    "Gilded Rupture", "Anchor Release", "Temporal Unwind", "Grace Horizon",
    "Doorless Leap", "Terminal Zero"
]

EMOTIONAL_STATES = {
    "Gold": {"core": "Calm", "modifier": 1, "desc": "Centering, clarity, reflection."},
    "Sapphire": {"core": "Strain", "modifier": 1, "desc": "Pressure, urgency, determination."},
    "Amethyst": {"core": "Break", "modifier": 2, "desc": "Rupture, overwhelm, fracture."},
    "Crimson": {"core": "Dissonance", "modifier": 0, "desc": "Contradiction, impossible choice."},
    "Teal": {"core": "Flow", "modifier": 0, "desc": "Adaptability, grace, surrender."},
    "Obsidian": {"core": "Void-Touch", "modifier": -1, "desc": "Numbness, emotional shutdown."},
    "Rose": {"core": "Rekindling", "modifier": 1, "desc": "Renewal, reclaimed purpose."}
}

class ArcanaEngine:
    """
    78-Card Ignition Arcana & DPIP Action Engine
    Simulates deck draws, emotional strain transitions, 2d6 action resolutions,
    and Monte Carlo angular vector interference.
    """
    def __init__(self):
        self.paradox = 0
        self.current_state = "Sapphire"  # Starting in Strain
        self.scars_accumulated = 0
        self.deck = self._build_deck()

    def _build_deck(self) -> List[Dict[str, str]]:
        deck = []
        for major in FLUX_MAJORS:
            deck.append({"type": "Major", "name": major, "chroma": "Prime"})
        for c in CHROMAS:
            for v in IDENTITY_VECTORS:
                deck.append({"type": "Minor", "name": f"{c} of {v}", "chroma": c, "vector": v})
        for reb in REBELLION_CARDS:
            deck.append({"type": "Rebellion", "name": reb, "chroma": "Paradox"})
        return deck

    def draw_card(self) -> Dict[str, str]:
        """Draws a random card from the 78-card Ignition Arcana deck."""
        return random.choice(self.deck)

    def roll_2d6(self) -> Tuple[int, int, int]:
        """Rolls 2d6 dice returning (die1, die2, total)."""
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return d1, d2, d1 + d2

    def resolve_action(self, action_name: str = "Resonance Pulse", stat_bonus: int = 1) -> Dict[str, Any]:
        """Resolves a tactical action using 2d6 + Stat + Emotional Modifier vs PBTA thresholds."""
        d1, d2, raw_sum = self.roll_2d6()
        emo_mod = EMOTIONAL_STATES[self.current_state]["modifier"]
        total = raw_sum + stat_bonus + emo_mod
        
        card = self.draw_card()
        paradox_gain = 0
        outcome = ""

        if total >= 10:
            outcome = "Strong Hit (Full Success)"
            if card["type"] == "Rebellion":
                paradox_gain = 1
        elif 7 <= total <= 9:
            outcome = "Weak Hit (Success with Complication)"
            paradox_gain = 1
        else:
            outcome = "Miss (Systemic Breakdown)"
            paradox_gain = 2
            self.scars_accumulated += 1

        self.paradox += paradox_gain
        break_occurred = False
        if self.paradox >= 5:
            break_occurred = True
            self.paradox = 0
            self.current_state = "Amethyst"  # Shift to Break state

        return {
            "action": action_name,
            "dice": [d1, d2],
            "raw_sum": raw_sum,
            "stat_bonus": stat_bonus,
            "emotional_state": self.current_state,
            "emotional_mod": emo_mod,
            "total_score": total,
            "outcome": outcome,
            "drawn_card": card,
            "paradox_delta": paradox_gain,
            "total_paradox": self.paradox,
            "break_occurred": break_occurred,
            "total_scars": self.scars_accumulated
        }

    def simulate_vector_interference(self, iterations: int = 500) -> Dict[str, Any]:
        """Monte Carlo simulation of chromatic vector interference across the 7x7 matrix."""
        results = {"Constructive": 0, "Orthogonal": 0, "Destructive": 0}
        for _ in range(iterations):
            c1, c2 = random.choice(CHROMAS), random.choice(CHROMAS)
            v1, v2 = random.choice(IDENTITY_VECTORS), random.choice(IDENTITY_VECTORS)
            
            if c1 == c2 and v1 == v2:
                results["Constructive"] += 1
            elif c1 == c2 or v1 == v2:
                results["Orthogonal"] += 1
            else:
                results["Destructive"] += 1

        return {
            "iterations": iterations,
            "distribution": results,
            "percentages": {k: round((v / iterations) * 100, 2) for k, v in results.items()}
        }

if __name__ == "__main__":
    arcana = ArcanaEngine()
    print(f"[ARCANA] Deck assembled with {len(arcana.deck)} cards.")
    act = arcana.resolve_action("Sanctuary Calibration", stat_bonus=2)
    print(f"  Action Result: {act['outcome']} (Total: {act['total_score']}) | Card: {act['drawn_card']['name']}")
    monte_carlo = arcana.simulate_vector_interference(1000)
    print(f"  Monte Carlo Interference: {monte_carlo['percentages']}")
