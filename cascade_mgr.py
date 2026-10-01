from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class DomainPhaseShiftEvent:
    event_id: str
    target_domain: str
    previous_epoch: int
    new_epoch: int
    rupture_trigger: str
    entropy_flushed: float
    residual_strain_baseline: float
    phase_shift_digest: str
    timestamp: str
    state_transformations: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CascadeManager:
    def __init__(self, domain_name: str = "A-Field Central Manifold") -> None:
        self.domain_name = domain_name
        self.current_epoch = 1
        self.events: List[DomainPhaseShiftEvent] = []

    def trigger_domain_phase_shift(
        self,
        current_strain: float,
        rupture_trigger: str,
        state_deltas: Optional[Dict[str, Any]] = None,
    ) -> DomainPhaseShiftEvent:
        prev_epoch = self.current_epoch
        self.current_epoch += 1
        event_id = f"CASCADE-{uuid4().hex[:8].upper()}"
        timestamp = datetime.now(timezone.utc).isoformat()
        entropy_flushed = current_strain
        residual_baseline = 0.5

        transformations = state_deltas or {}
        transformations.update({
            "epoch": self.current_epoch,
            "domain_phase": f"EPOCH_{self.current_epoch}",
            "metamorphic_squeeze_active": True,
            "tectonic_state": "POST_RUPTURE_VITRIFIED",
        })

        digest_payload = {
            "event_id": event_id,
            "target_domain": self.domain_name,
            "prev_epoch": prev_epoch,
            "new_epoch": self.current_epoch,
            "rupture_trigger": rupture_trigger,
            "entropy_flushed": entropy_flushed,
            "timestamp": timestamp,
        }
        digest = hashlib.sha256(json.dumps(digest_payload, sort_keys=True).encode("utf-8")).hexdigest()

        event = DomainPhaseShiftEvent(
            event_id=event_id,
            target_domain=self.domain_name,
            previous_epoch=prev_epoch,
            new_epoch=self.current_epoch,
            rupture_trigger=rupture_trigger,
            entropy_flushed=entropy_flushed,
            residual_strain_baseline=residual_baseline,
            phase_shift_digest=digest,
            timestamp=timestamp,
            state_transformations=transformations,
        )
        self.events.append(event)
        return event
