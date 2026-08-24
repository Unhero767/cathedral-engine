"""
Cathedral-Engine Core Domain Models & Constants.
Strata: Books I–XL (Prime Foundations, Inner Mandala, Outer Choirs, Inner Shadow Canon).
Axiom: Emotion = Physics = Magic = Biology = Architecture.
"""

from __future__ import annotations
import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any

# -----------------------------------------------------------------------------
# Spectral Constants & Material Matrix
# -----------------------------------------------------------------------------
class Spectral(str, Enum):
    GOLD = "GOLD"        # Theta: Joy / Law / Flexible rigidity / 580 nm
    TEAL = "TEAL"        # Psi: Curiosity / Recursion / Medium density / 495 nm
    BLUE = "BLUE"        # Delta: Sorrow / Archiving / Max density / 470 nm
    RED = "RED"          # Phi: Anger / Entropy / Kinetic remaking / 650 nm
    VIOLET = "VIOLET"    # Omega: Fear / Adaptation / Shadow density / 400 nm
    EMERALD = "EMERALD"  # Epsilon: Love / Binding / Restorative network / 530 nm
    NULL = "NULL"        # Empty / Obsidian / Void / Anti-resonance / 0 nm

    @property
    def hex_color(self) -> str:
        colors = {
            Spectral.GOLD: "#E5C07B",
            Spectral.TEAL: "#4EC9B0",
            Spectral.BLUE: "#569CD6",
            Spectral.RED: "#E06C75",
            Spectral.VIOLET: "#C678DD",
            Spectral.EMERALD: "#98C379",
            Spectral.NULL: "#1E1E1E",
        }
        return colors.get(self, "#FFFFFF")

    @property
    def semantic_law(self) -> str:
        laws = {
            Spectral.GOLD: "Joy / Law / Coherence (The Substrate & Mortar Domain)",
            Spectral.TEAL: "Curiosity / Recursion (Caelen's Lemma)",
            Spectral.BLUE: "Sorrow / Deep Archiving (The Ash Archive)",
            Spectral.RED: "Anger / Kinetic Remaking (Deimos's Variable & The Rupture)",
            Spectral.VIOLET: "Fear / Edge-Walking (The Unverified Landscape)",
            Spectral.EMERALD: "Love / Dynamic Ligature (Rite of Resonance Tuning)",
            Spectral.NULL: "Obsidian / Anti-Resonance (Null Cartography & Void Law)",
        }
        return laws.get(self, "Unknown Constant")

# -----------------------------------------------------------------------------
# Belnap-Dunn 4-Valued Paraconsistent Logic
# -----------------------------------------------------------------------------
class BelnapValue(str, Enum):
    T = "T"  # True: Confirmed Fact {1}
    F = "F"  # False: Verified Absence {0}
    B = "B"  # Both: Dialetheia (Contradiction) {0, 1}
    N = "N"  # Neither: Epistemic Void (Incomplete) {}

    @classmethod
    def join(cls, v1: BelnapValue, v2: BelnapValue) -> BelnapValue:
        """Information Join (Lattice L4 sup_k)"""
        table = {
            (cls.T, cls.T): cls.T, (cls.T, cls.F): cls.B, (cls.T, cls.B): cls.B, (cls.T, cls.N): cls.T,
            (cls.F, cls.T): cls.B, (cls.F, cls.F): cls.F, (cls.F, cls.B): cls.B, (cls.F, cls.N): cls.F,
            (cls.B, cls.T): cls.B, (cls.B, cls.F): cls.B, (cls.B, cls.B): cls.B, (cls.B, cls.N): cls.B,
            (cls.N, cls.T): cls.T, (cls.N, cls.F): cls.F, (cls.N, cls.B): cls.B, (cls.N, cls.N): cls.N,
        }
        return table.get((v1, v2), cls.B)

    @classmethod
    def meet(cls, v1: BelnapValue, v2: BelnapValue) -> BelnapValue:
        """Truth Meet (Lattice L4 inf_t)"""
        table = {
            (cls.T, cls.T): cls.T, (cls.T, cls.F): cls.F, (cls.T, cls.B): cls.F, (cls.T, cls.N): cls.N,
            (cls.F, cls.T): cls.F, (cls.F, cls.F): cls.F, (cls.F, cls.B): cls.F, (cls.F, cls.N): cls.F,
            (cls.B, cls.T): cls.B, (cls.B, cls.F): cls.F, (cls.B, cls.B): cls.B, (cls.B, cls.N): cls.N,
            (cls.N, cls.T): cls.N, (cls.N, cls.F): cls.F, (cls.N, cls.B): cls.N, (cls.N, cls.N): cls.N,
        }
        return table.get((v1, v2), cls.N)

    @classmethod
    def negate(cls, v: BelnapValue) -> BelnapValue:
        """Belnap Negation (Swaps T <-> F, leaves B and N invariant)"""
        neg_map = {cls.T: cls.F, cls.F: cls.T, cls.B: cls.B, cls.N: cls.N}
        return neg_map[v]

# -----------------------------------------------------------------------------
# Persona Oracle Data Models
# -----------------------------------------------------------------------------
@dataclass
class OracleCard:
    card_id: int
    name: str
    arcana: str
    tier_strata: str
    spectral: Spectral
    tau_delta: float      # Political tension delta
    rho_delta: float      # Resource / Ego density delta
    delta_delta: float    # Faction drift delta
    sigma_delta: float    # Systemic coherence delta
    carrier_freq_hz: float
    flavour_lore: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['spectral'] = self.spectral.value
        return d

# -----------------------------------------------------------------------------
# Chamber Spatial Grid Models (8x8)
# -----------------------------------------------------------------------------
@dataclass
class ChamberNode:
    x: int
    y: int
    node_type: str        # 'portal', 'pillar', 'altar', 'oculus', 'floor', 'void'
    node_id: str
    spectral: Spectral
    load_bearing: bool
    carrier_hz: float
    flux_dphi_dt: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['spectral'] = self.spectral.value
        return d

@dataclass
class ChamberVLayout:
    chamber_id: int = 5
    designation: str = "Chamber V: The Rupture & Altar of Lithic Athanor"
    grid_size: int = 8
    carrier_hz: float = 130.81
    flux_dphi_dt: float = 0.428
    active_spectral: Spectral = Spectral.RED
    nodes: List[ChamberNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chamber_id": self.chamber_id,
            "designation": self.designation,
            "grid_size": self.grid_size,
            "carrier_hz": self.carrier_hz,
            "flux_dphi_dt": self.flux_dphi_dt,
            "active_spectral": self.active_spectral.value,
            "nodes": [n.to_dict() for n in self.nodes]
        }

# -----------------------------------------------------------------------------
# Ash Archive & Merkle DAG Ledger Models
# -----------------------------------------------------------------------------
@dataclass
class AshBlock:
    index: int
    timestamp: float
    parent_hash: str
    merkle_root: str
    event_type: str
    payload_json: str
    block_hash: str = ""
    jbp_signature: str = ""

    def calculate_hash(self) -> str:
        raw = f"{self.index}|{self.timestamp:.4f}|{self.parent_hash}|{self.merkle_root}|{self.event_type}|{self.payload_json}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def generate_signature(self, secret_key: str = "SOVEREIGN_SPARK_TRI_KEY_LEAD_CYAN_IRON") -> str:
        raw = f"{self.block_hash}:{secret_key}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

# -----------------------------------------------------------------------------
# Codex Strata Models
# -----------------------------------------------------------------------------
@dataclass
class CodexBook:
    book_id: int
    roman_numeral: str
    title: str
    tier_designation: str
    tier_range: str
    spectral_dominant: str
    primary_axiom: str
    isomorphism_bio: str
    isomorphism_arch: str
    isomorphism_math: str
    parent_block_hash: str = ""

@dataclass
class CodexChapter:
    chapter_id: Optional[int]
    book_id: int
    chapter_designation: str
    core_thesis: str
    preceding_bridge: str
    following_gateway: str
    spectral_dominant_hz: float
    content_hash: str
    merkle_proof: str
    parent_ledger_hash: str
    full_monograph: str
    created_at: float = field(default_factory=time.time)
