from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


class StrainStatus(str, Enum):
    SUB_CRITICAL = "SUB_CRITICAL"
    CRITICAL = "CRITICAL"


@dataclass
class StrainReport:
    current_strain: float
    max_strain: float
    status: StrainStatus
    recent_delta: float
    accumulator_fraction: str


class StrainParadoxAccumulator:
    MAX_THRESHOLD: float = 5.0

    def __init__(self, initial_strain: float = 0.0) -> None:
        self.strain: float = max(0.0, min(initial_strain, self.MAX_THRESHOLD))
        self.history: List[Tuple[float, float, str]] = []

    @property
    def is_critical(self) -> bool:
        return self.strain >= self.MAX_THRESHOLD

    @property
    def status(self) -> StrainStatus:
        return StrainStatus.CRITICAL if self.is_critical else StrainStatus.SUB_CRITICAL

    def inject_strain(self, delta: float, reason: str = "Dialetheic Collision") -> StrainReport:
        self.strain = min(self.MAX_THRESHOLD, max(0.0, self.strain + delta))
        self.history.append((delta, self.strain, reason))
        return StrainReport(
            current_strain=self.strain,
            max_strain=self.MAX_THRESHOLD,
            status=self.status,
            recent_delta=delta,
            accumulator_fraction=f"{self.strain:.2f}/{self.MAX_THRESHOLD:.0f}",
        )

    def relieve_strain(self, amount: float, reason: str = "Scar Absorption") -> StrainReport:
        return self.inject_strain(-abs(amount), reason=reason)

    def reset_post_cascade(self, residual_baseline: float = 0.0) -> StrainReport:
        self.strain = max(0.0, min(residual_baseline, self.MAX_THRESHOLD))
        self.history.append((0.0, self.strain, "Post-Cascade Domain Reset"))
        return StrainReport(
            current_strain=self.strain,
            max_strain=self.MAX_THRESHOLD,
            status=self.status,
            recent_delta=0.0,
            accumulator_fraction=f"{self.strain:.2f}/{self.MAX_THRESHOLD:.0f}",
        )
