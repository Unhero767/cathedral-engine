"""
Ash Archive Repository Layer
Governs append-only block universe persistence with dialetheic contradiction preservation in PostgreSQL.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import UUID

import asyncpg


# ============================================================================
# Enums & Domain Entities
# ============================================================================

class SpectralConstant(str, Enum):
    GOLD_JOY = "GOLD_JOY"
    BLUE_SORROW = "BLUE_SORROW"
    RED_WRATH = "RED_WRATH"
    VIOLET_MYSTERY = "VIOLET_MYSTERY"
    GREEN_GROWTH = "GREEN_GROWTH"
    OBSIDIAN_SILENCE = "OBSIDIAN_SILENCE"


class DialetheicState(str, Enum):
    TRUE_ONLY = "TRUE_ONLY"
    FALSE_ONLY = "FALSE_ONLY"
    BOTH = "BOTH"
    NEITHER = "NEITHER"


@dataclass
class SpectralNode:
    node_id: UUID
    node_coordinate: str
    spectral_dominant: SpectralConstant
    consciousness_intensity: float
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class CathedralState:
    state_id: UUID
    node_id: UUID
    codex_cycle: int
    temporal_stratum: int
    state_truth: DialetheicState
    state_payload: dict[str, Any]
    valid_from: datetime
    valid_until: Optional[datetime]


@dataclass
class HarmonicScar:
    scar_id: UUID
    origin_state_id: UUID
    contradiction_matrix: dict[str, Any]
    scar_tension_vector: float
    spectral_frequency: SpectralConstant
    crystallized_at: datetime
    is_load_bearing: bool


# ============================================================================
# Domain Exceptions
# ============================================================================

class AshArchiveError(Exception):
    """Base exception for Ash Archive domain operations."""

class NodeNotFoundError(AshArchiveError):
    """Raised when an anchor node does not exist."""

class DuplicateNodeError(AshArchiveError):
    """Raised when an anchor coordinate is already registered."""

class ActiveStratumNotFoundError(AshArchiveError):
    """Raised when transitioning but no open/active stratum exists."""

class TemporalContinuityError(AshArchiveError):
    """Raised when temporal bounds violate chronological or exclusion continuity."""


# ============================================================================
# Repository Class
# ============================================================================

class AshArchiveRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def inscribe_node(
        self,
        node_coordinate: str,
        spectral_dominant: SpectralConstant,
        consciousness_intensity: float = 1.0,
    ) -> SpectralNode:
        query = """
            INSERT INTO spectral_nodes (node_coordinate, spectral_dominant, consciousness_intensity)
            VALUES ($1, $2, $3)
            RETURNING node_id, node_coordinate, spectral_dominant, consciousness_intensity, is_active, created_at, updated_at;
        """
        async with self.pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    query,
                    node_coordinate,
                    spectral_dominant.value if isinstance(spectral_dominant, Enum) else spectral_dominant,
                    consciousness_intensity,
                )
                return SpectralNode(**dict(row))
            except asyncpg.UniqueViolationError:
                raise DuplicateNodeError(f"Node coordinate '{node_coordinate}' already inscribed.")

    async def get_node_by_coordinate(self, node_coordinate: str) -> Optional[SpectralNode]:
        query = """
            SELECT node_id, node_coordinate, spectral_dominant, consciousness_intensity, is_active, created_at, updated_at
            FROM spectral_nodes
            WHERE node_coordinate = $1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, node_coordinate)
            return SpectralNode(**dict(row)) if row else None

    async def initialize_node_state(
        self,
        node_id: UUID,
        codex_cycle: int,
        temporal_stratum: int,
        state_truth: DialetheicState,
        state_payload: dict[str, Any],
        valid_from: Optional[datetime] = None,
    ) -> CathedralState:
        check_node = "SELECT node_id FROM spectral_nodes WHERE node_id = $1;"
        insert_query = """
            INSERT INTO cathedral_strata (node_id, codex_cycle, temporal_stratum, state_truth, state_payload, valid_from)
            VALUES ($1, $2, $3, $4, $5, COALESCE($6, clock_timestamp()))
            RETURNING state_id, node_id, codex_cycle, temporal_stratum, state_truth, state_payload, valid_from, valid_until;
        """
        async with self.pool.acquire() as conn:
            node_exists = await conn.fetchval(check_node, node_id)
            if not node_exists:
                raise NodeNotFoundError(f"Target anchor node '{node_id}' does not exist.")

            try:
                payload_json = json.dumps(state_payload)
                truth_val = state_truth.value if isinstance(state_truth, Enum) else state_truth
                row = await conn.fetchrow(
                    insert_query,
                    node_id,
                    codex_cycle,
                    temporal_stratum,
                    truth_val,
                    payload_json,
                    valid_from,
                )
                data = dict(row)
                data["state_payload"] = json.loads(data["state_payload"]) if isinstance(data["state_payload"], str) else data["state_payload"]
                return CathedralState(**data)
            except asyncpg.ExclusionViolationError as e:
                raise TemporalContinuityError(f"Temporal stratum overlap: {e}")

    async def transition_stratum(
        self,
        node_id: UUID,
        next_codex_cycle: int,
        next_temporal_stratum: int,
        next_state_truth: DialetheicState,
        next_state_payload: dict[str, Any],
        crystallize_scar: Optional[dict[str, Any]] = None,
    ) -> tuple[CathedralState, Optional[HarmonicScar]]:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # 1. Verify node existence
                node_exists = await conn.fetchval(
                    "SELECT node_id FROM spectral_nodes WHERE node_id = $1;", node_id
                )
                if not node_exists:
                    raise NodeNotFoundError(f"Anchor node '{node_id}' not found.")

                # 2. Acquire current active stratum with row lock
                active_row = await conn.fetchrow(
                    """
                    SELECT state_id, valid_from
                    FROM cathedral_strata
                    WHERE node_id = $1 AND valid_until IS NULL
                    FOR UPDATE;
                    """,
                    node_id,
                )
                if not active_row:
                    raise ActiveStratumNotFoundError(f"No active unclosed stratum found for node '{node_id}'.")

                active_state_id = active_row["state_id"]
                active_valid_from = active_row["valid_from"]
                now_utc = datetime.now(timezone.utc)

                if active_valid_from > now_utc:
                    raise TemporalContinuityError("Clock continuity failure: active stratum opened in the future.")

                # 3. Close the active stratum
                await conn.execute(
                    "UPDATE cathedral_strata SET valid_until = $1 WHERE state_id = $2;",
                    now_utc,
                    active_state_id,
                )

                # 4. Crystallize scar if provided
                scar_entity: Optional[HarmonicScar] = None
                if crystallize_scar:
                    scar_query = """
                        INSERT INTO harmonic_scars (
                            origin_state_id, contradiction_matrix, scar_tension_vector,
                            spectral_frequency, is_load_bearing
                        )
                        VALUES ($1, $2, $3, $4, $5)
                        RETURNING scar_id, origin_state_id, contradiction_matrix, scar_tension_vector,
                                  spectral_frequency, crystallized_at, is_load_bearing;
                    """
                    freq = crystallize_scar["spectral_frequency"]
                    scar_row = await conn.fetchrow(
                        scar_query,
                        active_state_id,
                        json.dumps(crystallize_scar["contradiction_matrix"]),
                        crystallize_scar["scar_tension_vector"],
                        freq.value if isinstance(freq, Enum) else freq,
                        crystallize_scar.get("is_load_bearing", True),
                    )
                    scar_data = dict(scar_row)
                    scar_data["contradiction_matrix"] = (
                        json.loads(scar_data["contradiction_matrix"])
                        if isinstance(scar_data["contradiction_matrix"], str)
                        else scar_data["contradiction_matrix"]
                    )
                    scar_entity = HarmonicScar(**scar_data)

                # 5. Inscribe the new active stratum
                truth_val = (
                    next_state_truth.value
                    if isinstance(next_state_truth, Enum)
                    else next_state_truth
                )
                new_state_row = await conn.fetchrow(
                    """
                    INSERT INTO cathedral_strata (
                        node_id, codex_cycle, temporal_stratum, state_truth, state_payload, valid_from
                    )
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING state_id, node_id, codex_cycle, temporal_stratum, state_truth,
                              state_payload, valid_from, valid_until;
                    """,
                    node_id,
                    next_codex_cycle,
                    next_temporal_stratum,
                    truth_val,
                    json.dumps(next_state_payload),
                    now_utc,
                )
                new_data = dict(new_state_row)
                new_data["state_payload"] = (
                    json.loads(new_data["state_payload"])
                    if isinstance(new_data["state_payload"], str)
                    else new_data["state_payload"]
                )
                return CathedralState(**new_data), scar_entity

    async def get_active_state(self, node_id: UUID) -> Optional[CathedralState]:
        query = """
            SELECT state_id, node_id, codex_cycle, temporal_stratum, state_truth, state_payload, valid_from, valid_until
            FROM cathedral_strata
            WHERE node_id = $1 AND valid_until IS NULL;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, node_id)
            if not row:
                return None
            data = dict(row)
            data["state_payload"] = json.loads(data["state_payload"]) if isinstance(data["state_payload"], str) else data["state_payload"]
            return CathedralState(**data)

    async def get_state_at_point_in_time(self, node_id: UUID, point_in_time: datetime) -> Optional[CathedralState]:
        query = """
            SELECT state_id, node_id, codex_cycle, temporal_stratum, state_truth, state_payload, valid_from, valid_until
            FROM cathedral_strata
            WHERE node_id = $1 
              AND tstzrange(valid_from, valid_until, '[)') @> $2::timestamptz;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, node_id, point_in_time)
            if not row:
                return None
            data = dict(row)
            data["state_payload"] = json.loads(data["state_payload"]) if isinstance(data["state_payload"], str) else data["state_payload"]
            return CathedralState(**data)
