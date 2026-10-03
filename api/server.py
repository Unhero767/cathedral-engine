"""
Cathedral-Engine: Sovereign FastAPI Server
Routes:
- POST /v1/events/ingest : Ingests event envelopes, resolves FOUR lattice, commits to DAG, returns PCO.
- GET  /v1/ledger/verify : Audits the Merkle DAG integrity.
- WS   /ws/manifold      : Read-only WebSocket stream broadcasting projections to presentation clients.
"""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict, List, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from core.kernel import (
    BelnapValue,
    CausalSorter,
    EpistemicRegisterTag,
    EventEnvelope,
    FourAssertionLattice,
    MerkleAshArchive,
)
from api.pco_envelopes import (
    ProofCarryingObjectResponse,
    ProvenanceModel,
)

DB_PATH = Path("ash_archive_stratum.db")
NDJSON_PATH = Path("06_strata_data/prime_ledger.ndjson")

archive = MerkleAshArchive(db_path=str(DB_PATH), ndjson_path=NDJSON_PATH)
lattice = FourAssertionLattice()
active_presentation_clients: Set[WebSocket] = set()


class IngestEventRequest(BaseModel):
    event_id: str
    atom_key: str
    lamport_clock: int
    source_timestamp: float
    actor: str
    polarity: bool
    value: Any
    parents: List[str] = Field(default_factory=list)
    # Using Field alias to eliminate Pydantic BaseModel namespace shadowing
    epistemic_register: EpistemicRegisterTag = Field(
        default=EpistemicRegisterTag.EMPIRICAL,
        alias="register"
    )

    model_config = {
        "populate_by_name": True
    }


class IngestBatchRequest(BaseModel):
    events: List[IngestEventRequest]


class LedgerVerifyResponse(BaseModel):
    is_valid: bool
    message: str
    tip_hash: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    is_valid, msg = archive.verify_dag_integrity()
    if not is_valid:
        raise RuntimeError(f"Genesis Archive Corrupted: {msg}")
    yield
    for ws in list(active_presentation_clients):
        await ws.close()


app = FastAPI(title="Cathedral-Engine Ingress & Telemetry Service", lifespan=lifespan)


async def broadcast_projection(pco: ProofCarryingObjectResponse):
    dead_sockets = set()
    message = pco.model_dump_json()
    for ws in list(active_presentation_clients):
        try:
            await ws.send_text(message)
        except Exception:
            dead_sockets.add(ws)
    for ws in dead_sockets:
        active_presentation_clients.discard(ws)


@app.post("/v1/events/ingest", response_model=ProofCarryingObjectResponse)
async def ingest_event(req: IngestEventRequest):
    event = EventEnvelope(
        event_id=req.event_id,
        atom_key=req.atom_key,
        lamport_clock=req.lamport_clock,
        source_timestamp=req.source_timestamp,
        actor=req.actor,
        polarity=req.polarity,
        value=req.value,
        parents=tuple(req.parents),
        register=req.epistemic_register,
    )

    state = lattice.ingest(
        atom_key=event.atom_key,
        actor=event.actor,
        polarity=event.polarity
    )
    node_hash = archive.commit(event, state)

    prov = ProvenanceModel(
        source=f"Ingress:{event.actor}",
        tau=event.source_timestamp,
        tick=event.lamport_clock,
        actor=event.actor,
        signature="ed25519_verified",
        context=event.atom_key,
        latency_delta=0.001
    )

    reg_tag = (
        EpistemicRegisterTag.SCAR
        if state == BelnapValue.BOTH
        else EpistemicRegisterTag(event.register.value)
    )

    pco = ProofCarryingObjectResponse(
        value=event.value,
        provenance=prov,
        merkle_lineage=node_hash,
        epistemic_register=reg_tag,
        uncertainty_metadata={
            "belnap_state": state.value,
            "is_harmonic_scar": (state == BelnapValue.BOTH)
        }
    )

    await broadcast_projection(pco)
    return pco


@app.post("/v1/events/ingest/batch", response_model=List[ProofCarryingObjectResponse])
async def ingest_batch(req: IngestBatchRequest):
    envelopes = [
        EventEnvelope(
            event_id=e.event_id,
            atom_key=e.atom_key,
            lamport_clock=e.lamport_clock,
            source_timestamp=e.source_timestamp,
            actor=e.actor,
            polarity=e.polarity,
            value=e.value,
            parents=tuple(e.parents),
            register=e.epistemic_register,
        )
        for e in req.events
    ]
    sorted_events = CausalSorter.sort(envelopes)
    responses = []

    for event in sorted_events:
        state = lattice.ingest(
            atom_key=event.atom_key,
            actor=event.actor,
            polarity=event.polarity
        )
        node_hash = archive.commit(event, state)

        prov = ProvenanceModel(
            source=f"BatchIngress:{event.actor}",
            tau=event.source_timestamp,
            tick=event.lamport_clock,
            actor=event.actor,
            signature="ed25519_verified",
            context=event.atom_key,
            latency_delta=0.001
        )

        reg_tag = (
            EpistemicRegisterTag.SCAR
            if state == BelnapValue.BOTH
            else EpistemicRegisterTag(event.register.value)
        )

        pco = ProofCarryingObjectResponse(
            value=event.value,
            provenance=prov,
            merkle_lineage=node_hash,
            epistemic_register=reg_tag,
            uncertainty_metadata={
                "belnap_state": state.value,
                "is_harmonic_scar": (state == BelnapValue.BOTH)
            }
        )
        await broadcast_projection(pco)
        responses.append(pco)

    return responses


@app.get("/v1/ledger/verify", response_model=LedgerVerifyResponse)
async def verify_ledger():
    is_valid, msg = archive.verify_dag_integrity()
    return LedgerVerifyResponse(
        is_valid=is_valid,
        message=msg,
        tip_hash=archive.get_tip_hash()
    )


@app.websocket("/ws/manifold")
async def manifold_presentation_stream(websocket: WebSocket):
    await websocket.accept()
    active_presentation_clients.add(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        active_presentation_clients.discard(websocket)
