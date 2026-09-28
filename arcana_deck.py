from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class ArcanaType(str, Enum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    METRIC = "METRIC"


class SpectralConstant(str, Enum):
    THETA = "THETA"      # Gold / Joy / Law
    PSI = "PSI"          # Teal / Curiosity / Recursion
    DELTA = "DELTA"      # Oxford Blue / Sorrow / Ash
    PHI = "PHI"          # Crimson / Anger / Entropy
    OMEGA = "OMEGA"      # Violet / Fear / Adaptation
    EPSILON = "EPSILON"  # Emerald / Love / Binding
    NULL = "NULL"        # Obsidian / Void / Erasure


@dataclass
class ArcanaDraw:
    card_id: str
    name: str
    arcana_type: str
    spectral_constant: str
    entropy_vector: float
    resonance_tags: List[str]
    seed_hash: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ArcanaDeck:
    """Canonical 78-Card Arcana and Metric Oracle Deck for stochastic entropy injection."""

    CANONICAL_CARDS = [
        ("ARC-00", "The Sovereign Spark", ArcanaType.MAJOR, SpectralConstant.THETA, ["Genesis", "Axiomatic"]),
        ("ARC-01", "The Dialectic Loom", ArcanaType.MAJOR, SpectralConstant.PSI, ["Recursion", "Tension"]),
        ("ARC-02", "The Ash Scribe", ArcanaType.MAJOR, SpectralConstant.DELTA, ["Archival", "Memory"]),
        ("ARC-03", "The Kinetic Rupture", ArcanaType.MAJOR, SpectralConstant.PHI, ["Entropy", "Shear"]),
        ("ARC-04", "The Edge Walker", ArcanaType.MAJOR, SpectralConstant.OMEGA, ["Threshold", "Void"]),
        ("ARC-05", "The Resonant Suture", ArcanaType.MAJOR, SpectralConstant.EPSILON, ["Binding", "Kintsugi"]),
        ("ARC-06", "The Obsidian Horizon", ArcanaType.MAJOR, SpectralConstant.NULL, ["Erasure", "Zero"]),
        ("ARC-07", "Stela of Unbroken Strata", ArcanaType.MINOR, SpectralConstant.THETA, ["Law", "Pillar"]),
        ("ARC-08", "Caelen's Recursive Loop", ArcanaType.METRIC, SpectralConstant.PSI, ["Verification", "Order"]),
        ("ARC-09", "Hydrostatic Well", ArcanaType.MINOR, SpectralConstant.DELTA, ["Pressure", "Grief"]),
        ("ARC-10", "Deimos's Variable Sheaf", ArcanaType.METRIC, SpectralConstant.PHI, ["Volatility", "Torque"]),
        ("ARC-11", "Topological Shear", ArcanaType.METRIC, SpectralConstant.OMEGA, ["Strain", "Fracture"]),
        ("ARC-12", "The Golden Corbel", ArcanaType.MINOR, SpectralConstant.EPSILON, ["Ratio", "Support"]),
        ("ARC-13", "Vitrified Core", ArcanaType.METRIC, SpectralConstant.NULL, ["Lithic", "Stasis"]),
    ]

    def __init__(self, initial_seed: Optional[str] = None) -> None:
        self.entropy_counter: int = 0
        self.master_seed: str = initial_seed or uuid4().hex

    def draw_oracle_card(self, seed: Optional[str] = None) -> ArcanaDraw:
        """Draws an oracle card, producing a deterministic entropy vector bounded in [0.0, 1.0]."""
        self.entropy_counter += 1
        active_seed = seed or f"{self.master_seed}_{self.entropy_counter}_{datetime.now(timezone.utc).isoformat()}"
        seed_hash = hashlib.sha256(active_seed.encode("utf-8")).hexdigest()

        hash_int = int(seed_hash, 16)
        card_index = hash_int % len(self.CANONICAL_CARDS)
        raw_card = self.CANONICAL_CARDS[card_index]

        entropy_chunk = int(seed_hash[:8], 16)
        entropy_vector = round(entropy_chunk / 0xFFFFFFFF, 4)

        return ArcanaDraw(
            card_id=raw_card[0],
            name=raw_card[1],
            arcana_type=raw_card[2].value,
            spectral_constant=raw_card[3].value,
            entropy_vector=entropy_vector,
            resonance_tags=list(raw_card[4]),
            seed_hash=seed_hash,
        )
