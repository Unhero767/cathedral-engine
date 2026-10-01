from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

GOLDEN_RATIO: float = 1.6180339887


@dataclass
class LoadBearingHarmonicScar:
    scar_id: str
    chamber: str
    axis: str
    trauma_type: str
    logical_valuation: str
    mass_a: float
    mass_b: float
    structural_capacity: float
    kintsugi_formula: str
    payload_json: Dict[str, Any]
    created_at: str
    scar_hash: str = field(default="")

    def __post_init__(self) -> None:
        if not self.scar_hash:
            self.scar_hash = self.compute_hash()

    def compute_hash(self) -> str:
        body = {
            "scar_id": self.scar_id,
            "chamber": self.chamber,
            "axis": self.axis,
            "trauma_type": self.trauma_type,
            "logical_valuation": self.logical_valuation,
            "mass_a": self.mass_a,
            "mass_b": self.mass_b,
            "structural_capacity": round(self.structural_capacity, 6),
            "kintsugi_formula": self.kintsugi_formula,
            "created_at": self.created_at,
        }
        return hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ScarAnchors:
    def __init__(self) -> None:
        self.scars: List[LoadBearingHarmonicScar] = []

    def crystallize_scar(
        self,
        chamber: str,
        axis: str,
        trauma_type: str,
        mass_a: float,
        mass_b: float,
        logical_valuation: str = "B",
        kintsugi_formula: str = "D_n -> R_n -> S_n -> K_n",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> LoadBearingHarmonicScar:
        capacity = (mass_a + mass_b) * GOLDEN_RATIO
        scar_id = f"SCAR-{uuid4().hex[:8].upper()}"
        created_at = datetime.now(timezone.utc).isoformat()
        payload = {
            "chamber": chamber,
            "axis": axis,
            "trauma_type": trauma_type,
            "valuation": logical_valuation,
            "mass_a": mass_a,
            "mass_b": mass_b,
            "load_bearing_capacity": capacity,
            "metadata": metadata or {},
        }
        scar = LoadBearingHarmonicScar(
            scar_id=scar_id,
            chamber=chamber,
            axis=axis,
            trauma_type=trauma_type,
            logical_valuation=logical_valuation,
            mass_a=mass_a,
            mass_b=mass_b,
            structural_capacity=capacity,
            kintsugi_formula=kintsugi_formula,
            payload_json=payload,
            created_at=created_at,
        )
        self.scars.append(scar)
        return scar
