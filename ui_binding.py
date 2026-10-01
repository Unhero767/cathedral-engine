from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class UIEventEnvelope:
    envelope_id: str
    event_type: str
    timestamp: str
    block_height: int
    merkle_root: str
    leaf_hash: str
    payload: Dict[str, Any]
    render_hints: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


class UIBindingDispatcher:
    """Authoritative dispatch adapter for Godot 4 and WebGL visual pipelines."""

    def __init__(self, client_id: str = "GODOT_AUTHORITATIVE_PORTAL") -> None:
        self.client_id = client_id
        self.dispatched_envelopes: List[UIEventEnvelope] = []

    def dispatch_state_update(
        self,
        committed_node: Any,
        arbiter_telemetry: Optional[Dict[str, str]] = None,
        spatial_telemetry: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        arbiter = arbiter_telemetry or {}
        spectral = arbiter.get("spectral_dominant", "THETA")
        has_cascade = committed_node.cascade_event is not None
        has_scars = len(committed_node.harmonic_scars) > 0

        render_hints = {
            "spectral_palette": spectral,
            "shader_pipeline": "LITHIC_PERMINERALIZED" if not has_cascade else "POST_CASCADE_VITRIFIED",
            "camera_shake_intensity": 1.0 if has_cascade else (0.4 if has_scars else 0.0),
            "kintsugi_glow": has_scars,
            "wireframe_overlay": committed_node.state_delta.get("strain", 0.0) >= 4.0,
        }

        envelope = UIEventEnvelope(
            envelope_id=f"EVT-UI-{committed_node.block_height:06d}",
            event_type="STATE_MERKLE_COMMIT",
            timestamp=datetime.now(timezone.utc).isoformat(),
            block_height=committed_node.block_height,
            merkle_root=committed_node.cumulative_state_digest,
            leaf_hash=committed_node.merkle_leaf_hash,
            payload={
                "state_delta": committed_node.state_delta,
                "scars": committed_node.harmonic_scars,
                "cascade": committed_node.cascade_event,
                "liturgy": arbiter.get("liturgical_synthesis", ""),
                "spatial": spatial_telemetry or {},
            },
            render_hints=render_hints,
        )

        self.dispatched_envelopes.append(envelope)
        return asdict(envelope)
