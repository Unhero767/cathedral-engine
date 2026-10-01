from __future__ import annotations

import random
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class ActionResolution:
    actor_id: str
    target_id: str
    raw_roll: int
    net_result: int
    is_success: bool
    dialetheic_contested: bool
    suggested_strain: float
    attribute_deltas: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CombatCore:
    """Mechanical combat and friction engine operating over d20 resolution matrices."""

    def __init__(self, deterministic_seed: Optional[int] = None) -> None:
        self._rng = random.Random(deterministic_seed) if deterministic_seed is not None else random.Random()

    def resolve_action(
        self,
        actor: Any,
        target: Any,
        action_type: str,
        modifier: int = 0,
        fixed_roll: Optional[int] = None,
    ) -> ActionResolution:
        raw_roll = fixed_roll if fixed_roll is not None else self._rng.randint(1, 20)
        actor_res = actor.stats.get("resonance", 10)
        target_ward = target.stats.get("ward", 10)

        net_result = raw_roll + (actor_res - 10) // 2 + modifier
        target_defense = 10 + (target_ward - 10) // 2

        attribute_deltas: Dict[str, int] = {}
        dialetheic_contested = False
        suggested_strain = 0.5

        if net_result == target_defense:
            dialetheic_contested = True
            is_success = True
            suggested_strain = 2.5
            attribute_deltas["integrity"] = -max(1, (actor_res // 3))
            attribute_deltas["recoil"] = -max(1, (target_ward // 4))
        elif net_result > target_defense:
            is_success = True
            margin = net_result - target_defense
            attribute_deltas["integrity"] = -max(1, margin + 2)
            suggested_strain = 0.5
        else:
            is_success = False
            attribute_deltas["recoil"] = -1
            suggested_strain = 0.25

        if raw_roll == 20:
            suggested_strain += 1.0
        elif raw_roll == 1:
            suggested_strain += 1.5
            dialetheic_contested = True

        return ActionResolution(
            actor_id=actor.entity_id,
            target_id=target.entity_id,
            raw_roll=raw_roll,
            net_result=net_result,
            is_success=is_success,
            dialetheic_contested=dialetheic_contested,
            suggested_strain=min(5.0, suggested_strain),
            attribute_deltas=attribute_deltas,
        )
