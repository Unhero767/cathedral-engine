from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

GENESIS_HASH: str = "0" * 64


class LexIViolationError(Exception):
    pass


@dataclass
class StateTransitionRequest:
    stratum: str
    domain: str
    operator: str
    state_delta: Dict[str, Any]
    harmonic_scars: List[Dict[str, Any]] = field(default_factory=list)
    cascade_event: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


@dataclass
class StateNode:
    node_id: str
    parent_hash: str
    merkle_leaf_hash: str
    timestamp: str
    block_height: int
    stratum: str
    domain: str
    operator: str
    state_delta: Dict[str, Any]
    harmonic_scars: List[Dict[str, Any]]
    cascade_event: Optional[Dict[str, Any]]
    cumulative_state_digest: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AshArchiveLedger:
    def __init__(self) -> None:
        self.nodes: List[StateNode] = []
        self.node_by_id: Dict[str, StateNode] = {}
        self.last_transition_time: float = 0.0
        self.current_merkle_root: str = GENESIS_HASH
        self.cumulative_state: Dict[str, Any] = {}

    def append_transition(self, request: StateTransitionRequest) -> StateNode:
        now = time.time()
        self.last_transition_time = now
        block_height = len(self.nodes)
        parent_hash = self.nodes[-1].merkle_leaf_hash if self.nodes else GENESIS_HASH

        self.cumulative_state.update(request.state_delta)
        cum_digest = hashlib.sha256(
            json.dumps(self.cumulative_state, sort_keys=True).encode("utf-8")
        ).hexdigest()

        leaf_payload = {
            "height": block_height,
            "parent": parent_hash,
            "delta": request.state_delta,
            "scars": [s.get("scar_hash", "") for s in request.harmonic_scars],
            "cascade": request.cascade_event.get("phase_shift_digest", "") if request.cascade_event else "",
            "cum_digest": cum_digest,
        }
        leaf_hash = hashlib.sha256(
            json.dumps(leaf_payload, sort_keys=True).encode("utf-8")
        ).hexdigest()

        node = StateNode(
            node_id=f"ASH-{uuid4().hex[:8].upper()}",
            parent_hash=parent_hash,
            merkle_leaf_hash=leaf_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
            block_height=block_height,
            stratum=request.stratum,
            domain=request.domain,
            operator=request.operator,
            state_delta=request.state_delta,
            harmonic_scars=request.harmonic_scars,
            cascade_event=request.cascade_event,
            cumulative_state_digest=cum_digest,
        )
        self.nodes.append(node)
        self.node_by_id[node.node_id] = node
        self._recompute_merkle_root()
        return node

    def mutate_node(self, node_id: str, new_data: Dict[str, Any]) -> None:
        raise LexIViolationError(f"LEX_I_PROHIBITION: Node '{node_id}' cannot be modified. Append-only.")

    def delete_node(self, node_id: str) -> None:
        raise LexIViolationError(f"LEX_I_PROHIBITION: Node '{node_id}' cannot be deleted. Permineralized.")

    def _recompute_merkle_root(self) -> None:
        if not self.nodes:
            self.current_merkle_root = GENESIS_HASH
            return
        hashes = [n.merkle_leaf_hash for n in self.nodes]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashlib.sha256((hashes[i] + hashes[i + 1]).encode("utf-8")).hexdigest()
                new_hashes.append(combined)
            hashes = new_hashes
        self.current_merkle_root = hashes[0]

    def verify_chain_integrity(self) -> bool:
        for i in range(len(self.nodes)):
            expected_parent = GENESIS_HASH if i == 0 else self.nodes[i - 1].merkle_leaf_hash
            if self.nodes[i].parent_hash != expected_parent:
                return False
        return True
