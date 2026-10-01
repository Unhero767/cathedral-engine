from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass
class TopologicalDatum:
    entity_id: str
    coordinates: Tuple[float, float, float]
    chamber_id: str
    stratum_tier: str
    anchor_status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class IndexRoom:
    """Spatial and topological ground datum for the Cathedral-Engine manifold."""

    DEFAULT_CHAMBER: str = "Chamber XXIV.04 - Central Transept"
    DEFAULT_STRATUM: str = "STRATUM_I_PRIME_FOUNDATIONS"

    def __init__(self, ground_district: str = "Genesis_Omega01") -> None:
        self.ground_district = ground_district
        self.spatial_registry: Dict[str, TopologicalDatum] = {}

    def locate_entity(self, entity_id: str) -> TopologicalDatum:
        if entity_id in self.spatial_registry:
            return self.spatial_registry[entity_id]

        raw_hash = hashlib.sha256(entity_id.encode("utf-8")).hexdigest()
        x = round((int(raw_hash[0:4], 16) % 2000 - 1000) / 10.0, 2)
        y = round((int(raw_hash[4:8], 16) % 2000 - 1000) / 10.0, 2)
        z = round((int(raw_hash[8:12], 16) % 500) / 10.0, 2)

        datum = TopologicalDatum(
            entity_id=entity_id,
            coordinates=(x, y, z),
            chamber_id=self.DEFAULT_CHAMBER,
            stratum_tier=self.DEFAULT_STRATUM,
            anchor_status="GROUNDED",
        )
        self.spatial_registry[entity_id] = datum
        return datum

    def translate_entity(
        self,
        entity_id: str,
        delta: Tuple[float, float, float],
        chamber_id: Optional[str] = None,
        anchor_status: str = "GROUNDED",
    ) -> TopologicalDatum:
        current = self.locate_entity(entity_id)
        new_coords = (
            round(current.coordinates[0] + delta[0], 2),
            round(current.coordinates[1] + delta[1], 2),
            round(current.coordinates[2] + delta[2], 2),
        )
        updated = TopologicalDatum(
            entity_id=entity_id,
            coordinates=new_coords,
            chamber_id=chamber_id or current.chamber_id,
            stratum_tier=current.stratum_tier,
            anchor_status=anchor_status,
        )
        self.spatial_registry[entity_id] = updated
        return updated
