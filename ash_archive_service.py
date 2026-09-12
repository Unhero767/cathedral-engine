"""
Ash Archive Service Layer & API Routes
Framework: FastAPI with asyncpg connection pooling and AshArchiveRepository.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Optional
from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field

# Domain models & repository
from ash_archive_repo import (
    ActiveStratumNotFoundError,
    AshArchiveError,
    AshArchiveRepository,
    CathedralState,
    DialetheicState,
    DuplicateNodeError,
    HarmonicScar,
    NodeNotFoundError,
    SpectralConstant,
    SpectralNode,
    TemporalContinuityError,
)

# ============================================================================
# Pydantic Schemas
# ============================================================================

class InscribeNodeRequest(BaseModel):
    node_coordinate: str = Field(..., max_length=128, example="CHAMBER-07-SANCTUM")
    spectral_dominant: SpectralConstant = Field(..., example=SpectralConstant.GOLD_JOY)
    consciousness_intensity: float = Field(default=1.0, ge=0.0, example=1.618)


class SpectralNodeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    node_id: UUID
    node_coordinate: str
    spectral_dominant: SpectralConstant
    consciousness_intensity: float
    is_active: bool
    created_at: datetime
    updated_at: datetime


class InitializeStateRequest(BaseModel):
    codex_cycle: int = Field(..., ge=0, example=1)
    temporal_stratum: int = Field(..., ge=0, example=0)
    state_truth: DialetheicState = Field(default=DialetheicState.TRUE_ONLY, example=DialetheicState.TRUE_ONLY)
    state_payload: dict[str, Any] = Field(default_factory=dict, example={"phase": "ingress", "resonance": 1.0})
    valid_from: Optional[datetime] = Field(default=None, description="Defaults to clock_timestamp() if omitted")


class CrystallizeScarPayload(BaseModel):
    contradiction_matrix: dict[str, Any] = Field(..., example={"thesis": True, "antithesis": True})
    scar_tension_vector: float = Field(..., example=0.875)
    spectral_frequency: SpectralConstant = Field(..., example=SpectralConstant.BLUE_SORROW)
    is_load_bearing: bool = Field(default=True)


class TransitionStratumRequest(BaseModel):
    next_codex_cycle: int = Field(..., ge=0, example=1)
    next_temporal_stratum: int = Field(..., ge=0, example=1)
    next_state_truth: DialetheicState = Field(..., example=DialetheicState.BOTH)
    next_state_payload: dict[str, Any] = Field(..., example={"phase": "dialetheic_collision"})
    crystallize_scar: Optional[CrystallizeScarPayload] = None


class CathedralStateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    state_id: UUID
    node_id: UUID
    codex_cycle: int
    temporal_stratum: int
    state_truth: DialetheicState
    state_payload: dict[str, Any]
    valid_from: datetime
    valid_until: Optional[datetime]


class HarmonicScarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    scar_id: UUID
    origin_state_id: UUID
    contradiction_matrix: dict[str, Any]
    scar_tension_vector: float
    spectral_frequency: SpectralConstant
    crystallized_at: datetime
    is_load_bearing: bool


class TransitionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    state: CathedralStateResponse
    crystallized_scar: Optional[HarmonicScarResponse] = None


# ============================================================================
# API Router Definition & Dependency Injection
# ============================================================================

router = APIRouter(prefix="/v1/archive", tags=["Ash Archive Stratum"])


def get_repository(request: Request) -> AshArchiveRepository:
    """Dependency injector extracting the repository from the active app state pool."""
    repo: Optional[AshArchiveRepository] = getattr(request.app.state, "ash_repo", None)
    if repo is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ash Archive State Store pool is uninitialized.",
        )
    return repo


@router.post(
    "/nodes",
    response_model=SpectralNodeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Inscribe a Spectral Anchor Node",
)
async def inscribe_node(
    payload: InscribeNodeRequest,
    repo: AshArchiveRepository = Depends(get_repository),
) -> SpectralNodeResponse:
    try:
        node = await repo.inscribe_node(
            node_coordinate=payload.node_coordinate,
            spectral_dominant=payload.spectral_dominant,
            consciousness_intensity=payload.consciousness_intensity,
        )
        return SpectralNodeResponse.model_validate(node)
    except DuplicateNodeError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Node with coordinate '{payload.node_coordinate}' already exists.",
        )


@router.get(
    "/nodes/{node_coordinate}",
    response_model=SpectralNodeResponse,
    summary="Fetch Spectral Node by Coordinate",
)
async def get_node_by_coordinate(
    node_coordinate: str,
    repo: AshArchiveRepository = Depends(get_repository),
) -> SpectralNodeResponse:
    node = await repo.get_node_by_coordinate(node_coordinate)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spectral node '{node_coordinate}' not found.",
        )
    return SpectralNodeResponse.model_validate(node)


@router.post(
    "/nodes/{node_id}/state/init",
    response_model=CathedralStateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initialize Baseline Node Stratum",
)
async def initialize_node_state(
    node_id: UUID,
    payload: InitializeStateRequest,
    repo: AshArchiveRepository = Depends(get_repository),
) -> CathedralStateResponse:
    try:
        valid_from = payload.valid_from
        if valid_from is not None:
            valid_from = (
                valid_from.replace(tzinfo=timezone.utc)
                if valid_from.tzinfo is None
                else valid_from.astimezone(timezone.utc)
            )

        state = await repo.initialize_node_state(
            node_id=node_id,
            codex_cycle=payload.codex_cycle,
            temporal_stratum=payload.temporal_stratum,
            state_truth=payload.state_truth,
            state_payload=payload.state_payload,
            valid_from=valid_from,
        )
        return CathedralStateResponse.model_validate(state)
    except NodeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TemporalContinuityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post(
    "/nodes/{node_id}/state/transition",
    response_model=TransitionResponse,
    status_code=status.HTTP_200_OK,
    summary="Atomically Transition Temporal Stratum",
)
async def transition_stratum(
    node_id: UUID,
    payload: TransitionStratumRequest,
    repo: AshArchiveRepository = Depends(get_repository),
) -> TransitionResponse:
    scar_dict = payload.crystallize_scar.model_dump() if payload.crystallize_scar else None
    try:
        new_state, scar = await repo.transition_stratum(
            node_id=node_id,
            next_codex_cycle=payload.next_codex_cycle,
            next_temporal_stratum=payload.next_temporal_stratum,
            next_state_truth=payload.next_state_truth,
            next_state_payload=payload.next_state_payload,
            crystallize_scar=scar_dict,
        )
        return TransitionResponse(
            state=CathedralStateResponse.model_validate(new_state),
            crystallized_scar=HarmonicScarResponse.model_validate(scar) if scar else None,
        )
    except NodeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ActiveStratumNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except TemporalContinuityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get(
    "/nodes/{node_id}/state/active",
    response_model=CathedralStateResponse,
    summary="Retrieve Active Unclosed Stratum",
)
async def get_active_state(
    node_id: UUID,
    repo: AshArchiveRepository = Depends(get_repository),
) -> CathedralStateResponse:
    state = await repo.get_active_state(node_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No active unclosed stratum exists for node '{node_id}'.",
        )
    return CathedralStateResponse.model_validate(state)


@router.get(
    "/nodes/{node_id}/state/temporal",
    response_model=CathedralStateResponse,
    summary="Query Point-in-Time State via GiST Index",
)
async def get_state_at_point_in_time(
    node_id: UUID,
    point_in_time: datetime = Query(
        ...,
        description="Target ISO timestamp for block-universe point-in-time state resolution (normalized to UTC)",
        example="2026-09-09T11:49:41Z",
    ),
    repo: AshArchiveRepository = Depends(get_repository),
) -> CathedralStateResponse:
    normalized_pit = (
        point_in_time.replace(tzinfo=timezone.utc)
        if point_in_time.tzinfo is None
        else point_in_time.astimezone(timezone.utc)
    )

    state = await repo.get_state_at_point_in_time(node_id, normalized_pit)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No stratum existed for node '{node_id}' at {normalized_pit.isoformat()}.",
        )
    return CathedralStateResponse.model_validate(state)


# ============================================================================
# Application Lifecycle & Harness Setup
# ============================================================================

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/cathedral"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages connection pool creation and cleanup for the application."""
    pool = await asyncpg.create_pool(
        dsn=DATABASE_URL,
        min_size=5,
        max_size=20,
        command_timeout=60.0,
    )
    app.state.ash_repo = AshArchiveRepository(pool)
    yield
    await pool.close()


app = FastAPI(
    title="Cathedral-Engine Ash Archive Stratum Service",
    version="1.0.0",
    description="Append-only block universe persistence with dialetheic contradiction preservation.",
    lifespan=lifespan,
)

app.include_router(router)
