from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .arcana_deck import ArcanaDeck, ArcanaDraw
from .belnap_dunn import BelnapDunnEvaluator, BelnapValue
from .combat_core import CombatCore, ActionResolution
from .strain_paradox import StrainParadoxAccumulator, StrainStatus
from .scar_anchors import ScarAnchors, LoadBearingHarmonicScar
from .cascade_mgr import CascadeManager, DomainPhaseShiftEvent
from .cal_engine import CALEngine, InvariantValidationResult
from .ash_archive import AshArchiveLedger, StateNode, StateTransitionRequest
from .arbiter_magister import ArbiterMagister
from .index_room import IndexRoom, TopologicalDatum
from .ui_binding import UIBindingDispatcher


@dataclass
class EntityAST:
    entity_id: str
    name: str
    faction: str
    stats: Dict[str, int]
    max_stats: Dict[str, int]
    status_flags: List[str] = field(default_factory=list)
    location: str = "Central Manifold"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StateKernel:
    """Authoritative 12-Phase Core Kernel for the Cathedral-Engine runtime."""

    def __init__(
        self,
        domain: str = "Cathedral-Engine Prime",
        stratum: str = "STRATUM_I_PRIME_FOUNDATIONS",
    ) -> None:
        self.domain = domain
        self.stratum = stratum
        self.turn: int = 1
        self.phase: str = "INITIALIZED"

        self.entities: Dict[str, EntityAST] = {}
        self.logic_propositions: Dict[str, str] = {}
        self.world_attributes: Dict[str, Any] = {
            "epoch": 1,
            "domain_phase": "EPOCH_1",
            "active_district": "Genesis_Omega01",
        }

        # 12-Phase Pipeline Instantiations
        self.arcana_deck = ArcanaDeck()
        self.logic_evaluator = BelnapDunnEvaluator()
        self.combat_core = CombatCore()
        self.strain_accumulator = StrainParadoxAccumulator(0.0)
        self.scar_anchors = ScarAnchors()
        self.cascade_mgr = CascadeManager(domain_name=domain)
        self.cal_engine = CALEngine(strict_lex_i=True)
        self.ash_archive = AshArchiveLedger()
        self.arbiter_magister = ArbiterMagister()
        self.index_room = IndexRoom()
        self.ui_dispatcher = UIBindingDispatcher()

    def register_entity(self, entity: EntityAST) -> TopologicalDatum:
        self.entities[entity.entity_id] = entity
        return self.index_room.locate_entity(entity.entity_id)

    def get_canonical_state(self) -> Dict[str, Any]:
        return {
            "turn": self.turn,
            "phase": self.phase,
            "world": dict(self.world_attributes),
            "strain": self.strain_accumulator.strain,
            "logic_propositions": dict(self.logic_propositions),
            "entities": {k: e.to_dict() for k, e in self.entities.items()},
            "scars_count": len(self.scar_anchors.scars),
            "merkle_root": self.ash_archive.current_merkle_root,
        }

    def execute_operational_turn(
        self,
        action_name: str,
        actor_id: Optional[str] = None,
        target_id: Optional[str] = None,
        assertion_val: str = "T",
        counter_assertion_val: Optional[str] = None,
        oracle_seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Phase 10: Arcana Deck
        oracle_draw: ArcanaDraw = self.arcana_deck.draw_oracle_card(seed=oracle_seed)

        # Phase 03: Combat Core
        combat_resolution: Optional[ActionResolution] = None
        if actor_id and target_id and actor_id in self.entities and target_id in self.entities:
            combat_resolution = self.combat_core.resolve_action(
                actor=self.entities[actor_id],
                target=self.entities[target_id],
                action_type=action_name,
            )
            target_entity = self.entities[target_id]
            for attr, d_val in combat_resolution.attribute_deltas.items():
                target_entity.stats[attr] = target_entity.stats.get(attr, 10) + d_val

            if combat_resolution.dialetheic_contested:
                counter_assertion_val = "T"

        # Phase 02: Belnap-Dunn Logic Layer
        if counter_assertion_val:
            collision = self.logic_evaluator.process_dialetheic_collision(
                assertion_val, counter_assertion_val
            )
            resolved_logic = collision["resolved_state"]
            tensor_strain = collision["tensor_strain"]
        else:
            resolved_logic = assertion_val
            tensor_strain = 0.5 if assertion_val in {"T", "F"} else 0.0

        prop_key = f"prop_turn_{self.turn}_{action_name}"
        self.logic_propositions[prop_key] = resolved_logic

        # Phase 04: Strain/Paradox Accumulator & Bifurcation Gate
        net_strain_injection = tensor_strain
        if combat_resolution:
            net_strain_injection = max(net_strain_injection, combat_resolution.suggested_strain)

        strain_report = self.strain_accumulator.inject_strain(
            net_strain_injection, reason=f"Turn {self.turn}: {action_name}"
        )

        staged_scars: List[Dict[str, Any]] = []
        cascade_event: Optional[Dict[str, Any]] = None

        if strain_report.status == StrainStatus.CRITICAL:
            # Phase 08: Cascade Manager
            shift_event = self.cascade_mgr.trigger_domain_phase_shift(
                current_strain=self.strain_accumulator.strain,
                rupture_trigger=f"Dialectic saturation during {action_name} [Oracle: {oracle_draw.name}]",
                state_deltas={"turn_ruptured": self.turn, "oracle_seed": oracle_draw.seed_hash},
            )
            cascade_event = shift_event.to_dict()
            self.world_attributes["epoch"] = shift_event.new_epoch
            self.world_attributes.update(shift_event.state_transformations)
            self.strain_accumulator.reset_post_cascade(
                residual_baseline=shift_event.residual_strain_baseline
            )
        else:
            # Phase 05: Scar Anchors
            if resolved_logic == "B":
                scar = self.scar_anchors.crystallize_scar(
                    chamber=self.world_attributes.get("active_district", "Central Transept"),
                    axis="Suṣumṇā Central Axis",
                    trauma_type=f"DIALETHEIC_COLLISION_{action_name.upper()}",
                    mass_a=1.0 + (oracle_draw.entropy_vector * 0.5),
                    mass_b=1.0,
                    logical_valuation="B",
                    metadata={"oracle_card": oracle_draw.card_id},
                )
                staged_scars.append(scar.to_dict())
                self.strain_accumulator.relieve_strain(0.5, reason="Scar Anchor Crystallization")

        # Phase 07: CAL Engine
        current_canonical = self.get_canonical_state()
        proposed_delta = {
            "turn": self.turn,
            "action": action_name,
            "strain": self.strain_accumulator.strain,
            "logic_propositions": dict(self.logic_propositions),
            "world": dict(self.world_attributes),
            "oracle_draw": oracle_draw.to_dict(),
        }

        cal_result: InvariantValidationResult = self.cal_engine.validate_transition(
            current_state=current_canonical,
            proposed_delta=proposed_delta,
            harmonic_scars=staged_scars,
            cascade_event=cascade_event,
        )

        if not cal_result.is_valid:
            raise RuntimeError(f"CAL_INVARIANT_REJECTION: {cal_result.violations}")

        # Phase 06: Ash Archive WAL & Merkle DAG
        transition_req = StateTransitionRequest(
            stratum=self.stratum,
            domain=self.domain,
            operator="Sovereign Operator",
            state_delta=cal_result.sanitized_delta,
            harmonic_scars=staged_scars,
            cascade_event=cascade_event,
            notes=f"Turn {self.turn} executed under Lex I with Oracle [{oracle_draw.name}].",
        )
        committed_node: StateNode = self.ash_archive.append_transition(transition_req)

        # Downstream Telemetry & Egress
        arbiter_telemetry = self.arbiter_magister.ingest_committed_node(committed_node)

        spatial_telemetry: Dict[str, Any] = {}
        if actor_id:
            loc = self.index_room.translate_entity(actor_id, delta=(1.0, 0.0, 0.0))
            spatial_telemetry[actor_id] = loc.to_dict()

        ui_envelope = self.ui_dispatcher.dispatch_state_update(
            committed_node=committed_node,
            arbiter_telemetry=arbiter_telemetry,
            spatial_telemetry=spatial_telemetry,
        )

        self.turn += 1
        self.phase = "PLAYING"

        return {
            "turn_committed": committed_node.block_height,
            "node_id": committed_node.node_id,
            "leaf_hash": committed_node.merkle_leaf_hash,
            "merkle_root": self.ash_archive.current_merkle_root,
            "oracle_drawn": oracle_draw.name,
            "resolved_logic": resolved_logic,
            "strain": self.strain_accumulator.strain,
            "scars_created": len(staged_scars),
            "cascade_occurred": cascade_event is not None,
            "liturgy": arbiter_telemetry["liturgical_synthesis"],
            "ui_event_id": ui_envelope["envelope_id"],
            "archive_chain_valid": self.ash_archive.verify_chain_integrity(),
        }
