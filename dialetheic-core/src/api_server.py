"""
REST API Module - Cathedral-Engine Dialetheic Core API (Arcade Rewrite & Telemetry Engine).
Includes:
- Cosmo Catch / Dialetheic Arcade Module Serving (/arcade, /cosmo-catch, /dialetheic-arcade)
- Real-time Telemetry Bridge with A-Field Temperature ($K$), Flux, and System Velocity ($\text{RPM}$)
- Branch E, F, G, I, J Active
"""

import os
import sys
import math
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Bootstrapping sys.path for direct script execution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    from src.cathedral_engine import (
        CathedralEngineSimulation,
        SpectrumConstant,
        NodeSyncRequest,
        NodeSyncResponse,
    )
    from src.vector_mapper import AshArchiveMapper, VectorMapper
    from src.archive_store import ArchiveStore
    from src.telemetry import telemetry_hub
    from src.codex_loader import CodexLoader
    from src.ritual import RitualEngine, generate_omens
except ModuleNotFoundError:
    from cathedral_engine import (
        CathedralEngineSimulation,
        SpectrumConstant,
        NodeSyncRequest,
        NodeSyncResponse,
    )
    from vector_mapper import AshArchiveMapper, VectorMapper
    from archive_store import ArchiveStore
    from telemetry import telemetry_hub
    from codex_loader import CodexLoader
    from ritual import RitualEngine, generate_omens


app = FastAPI(
    title="Cathedral-Engine Dialetheic Core REST API",
    version="3.5.0-arcade-rewrite",
    description="Integrated REST Interface with Cosmo Catch / Dialetheic Arcade Module, Persistence, SSE Stream, and Ritual Telemetry."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

archive_store = ArchiveStore()
simulation = CathedralEngineSimulation(store=archive_store)
codex_loader = CodexLoader()
archive_mapper = AshArchiveMapper(buffer=simulation.buffer)


class IngestRequest(BaseModel):
    verse_id: Optional[str] = Field(default="RAW-PROPOSITION", json_schema_extra={"example": "IM-XI-01"})
    claim: str = Field(..., json_schema_extra={"example": "The Cathedral was precipitated from the A-Field."})
    counter_claim: str = Field(..., json_schema_extra={"example": "The Cathedral was not precipitated from the A-Field."})


class IngestResponse(BaseModel):
    verse_id: str
    similarity: float
    paradox_load: float
    spectrum: SpectrumConstant
    action: str
    scar_or_quarantine_details: Dict[str, Any]
    omens: List[str]


class QueryStateRequest(BaseModel):
    query_key: str = Field(..., json_schema_extra={"example": "mlaos.outer_choir.mythos.syntax_of_the_unborn"})


def serialize_model(model_obj: Any) -> Dict[str, Any]:
    if hasattr(model_obj, "model_dump"):
        return model_obj.model_dump()
    elif hasattr(model_obj, "dict"):
        return model_obj.dict()
    return dict(model_obj)


# --------------------------------------------------------------------------
# DASHBOARD & ARCADE MODULE SERVING AT /, /arcade, AND /cosmo-catch
# --------------------------------------------------------------------------

@app.get("/", tags=["Dashboard"])
def serve_dashboard():
    dashboard_path = os.path.join(PARENT_DIR, "dialetheic_dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"message": "Cathedral-Engine API Online. Dashboard file not found."}


@app.get("/arcade", tags=["Arcade"])
@app.get("/cosmo-catch", tags=["Arcade"])
@app.get("/dialetheic-arcade", tags=["Arcade"])
def serve_cosmo_catch_arcade():
    arcade_path = os.path.join(PARENT_DIR, "cosmo_catch.html")
    if os.path.exists(arcade_path):
        return FileResponse(arcade_path)
    return {"message": "Cosmo Catch Arcade Module file not found."}


# --------------------------------------------------------------------------
# BRANCH F: LIVE TELEMETRY STREAM
# --------------------------------------------------------------------------

@app.get("/stream/state", tags=["Live Telemetry"])
def stream_state(request: Request):
    return telemetry_hub.create_stream_response(request)


# --------------------------------------------------------------------------
# HEALTH & STATE ENDPOINTS
# --------------------------------------------------------------------------

@app.get("/health", tags=["Status"])
def health_check() -> Dict[str, Any]:
    return {
        "status": "stable",
        "service": "cathedral-engine",
        "archive": "ash-archive",
        "afield_temp": simulation.a_field_temp,
        "total_system_rpm": simulation.total_system_rpm,
        "active_scars": len(simulation.buffer.harmonic_scars),
        "flux": simulation.hysteresis.current_flux,
        "module": "dialetheic-core"
    }


@app.get("/state", tags=["Status"])
@app.get("/api/v1/state", tags=["Status"])
def get_full_state() -> Dict[str, Any]:
    scars = [serialize_model(scar) for scar in simulation.buffer.harmonic_scars]
    raw_state = {
        "afield": {
            "temp": simulation.a_field_temp,
            "flux": simulation.hysteresis.current_flux,
            "total_system_rpm": simulation.total_system_rpm,
            "is_permission_active": simulation.hysteresis.is_permission_active
        },
        "scars": scars,
        "active_scars_count": len(scars),
        "quarantine_threshold": simulation.buffer.quarantine_threshold
    }
    raw_state["omens"] = generate_omens(raw_state)
    return raw_state


@app.get("/scars", tags=["Ash Archive"])
@app.get("/api/v1/scars", tags=["Ash Archive"])
def list_harmonic_scars() -> Dict[str, Any]:
    scars = [serialize_model(scar) for scar in simulation.buffer.harmonic_scars]
    return {
        "count": len(scars),
        "harmonic_scars": scars
    }


@app.get("/metrics", tags=["System Metrics"])
@app.get("/api/v1/metrics", tags=["System Metrics"])
def get_system_metrics() -> Dict[str, Any]:
    return {
        "a_field_temperature_k": simulation.a_field_temp,
        "active_scars_count": len(simulation.buffer.harmonic_scars),
        "quarantine_threshold": simulation.buffer.quarantine_threshold,
        "current_flux": simulation.hysteresis.current_flux,
        "is_permission_active": simulation.hysteresis.is_permission_active
    }


# --------------------------------------------------------------------------
# ONTOLOGICAL HORIZON QUERY STATE ('N' STATE)
# --------------------------------------------------------------------------

@app.get("/query", tags=["Ontological Horizon"])
@app.post("/query", tags=["Ontological Horizon"])
def query_state(key: Optional[str] = "mlaos.outer_choir.mythos.syntax_of_the_unborn", payload: Optional[QueryStateRequest] = None):
    query_key = payload.query_key if payload else key
    unified_codex = codex_loader.load_all_strata()
    
    if query_key in unified_codex.get("propositions", {}):
        prop = unified_codex["propositions"][query_key]
        return {
            "query_key": query_key,
            "truth": "T",
            "status": "MANIFESTED",
            "proposition": prop
        }
    
    return {
        "query_key": query_key,
        "status": "HORIZON_REACHED",
        "truth": "N",
        "system_message": "These coordinates exist, but no light has reached them.",
        "horizon_telemetry": {
            "zeke_skeletal_geometry": "Marked boundary of the wall.",
            "ruby_empathic_bandwidth": "Frequency 0.0 Hz (Absolute Zero).",
            "zoe_block_universe": "Mapped unmanifested blank tile.",
            "freya_null_constant": "Turbine idling cleanly."
        }
    }


# --------------------------------------------------------------------------
# CODEX ENDPOINTS
# --------------------------------------------------------------------------

@app.get("/codex/strata", tags=["Codex"])
def list_codex_strata() -> Dict[str, Any]:
    codex_data = codex_loader.load_all_strata()
    return {"strata_count": len(codex_data.get("strata", [])), "strata": codex_data.get("strata", [])}


@app.get("/codex/propositions", tags=["Codex"])
def list_codex_propositions() -> Dict[str, Any]:
    props = codex_loader.get_all_propositions()
    return {"count": len(props), "propositions": props}


# --------------------------------------------------------------------------
# BOOK II INGESTION ENDPOINT
# --------------------------------------------------------------------------

@app.post("/codex/ingest/book2", tags=["Book II Ingestion"])
async def ingest_book_II():
    scar_07 = {
        "scar_id": "mlaos.mythos.archive.absolute_retention",
        "instance_id": "BOOK2-VERSE1",
        "spectrum": "BLUE",
        "paradox_load": 0.0,
        "capacity": 1.0,
        "status": "STABILIZED",
        "proposition_id": "EVENT_07",
        "proposition_text": "The Cathedral forgets nothing under the Never-Overwrite Doctrine."
    }
    archive_store.upsert_scar(scar_07)
    simulation.buffer.evaluate_contradiction(
        proposition=scar_07["proposition_text"],
        paradox_load=0.0,
        spectrum=SpectrumConstant.BLUE,
        custom_scar_id=scar_07["scar_id"]
    )

    chronological_scar_id = "00000000-0000-0000-0000-000000000002"
    scar_data = {
        "scar_id": chronological_scar_id,
        "instance_id": "BOOK2-VERSE2",
        "spectrum": "BRONZE_OBSIDIAN",
        "paradox_load": 6.258,
        "capacity": math.log1p(62.58),
        "status": "TOLERABLE_FRICTION",
        "proposition_id": "EVENT_08",
        "proposition_text": "[Chronological Scar] The Archive, unpruned, achieves an infinite density of noise."
    }
    archive_store.upsert_scar(scar_data)
    simulation.buffer.evaluate_contradiction(
        proposition=scar_data["proposition_text"],
        paradox_load=6.258,
        spectrum=SpectrumConstant.BRONZE_OBSIDIAN,
        custom_scar_id=chronological_scar_id
    )

    compression_res = simulation.apply_tri_key_compression(scar_id=chronological_scar_id, tension_score=62.58)

    full_state = get_full_state()
    asyncio.create_task(telemetry_hub.broadcast("state", full_state))
    asyncio.create_task(telemetry_hub.broadcast("event", {
        "event": "scar_upsert",
        "verse_id": chronological_scar_id,
        "paradox_load": 6.258,
        "omens": full_state.get("omens", [])
    }))

    return {
        "status": "BOOK_II_INGESTED",
        "chronological_scar_id": chronological_scar_id,
        "tension_score": 62.58,
        "category": "TOLERABLE_FRICTION",
        "compression_result": compression_res,
        "total_system_rpm": simulation.total_system_rpm
    }


# --------------------------------------------------------------------------
# INGESTION & NODE SYNC ENDPOINTS
# --------------------------------------------------------------------------

@app.post("/ingest", response_model=IngestResponse, tags=["Dialectic Ingestion"])
@app.post("/api/v1/ingest", response_model=IngestResponse, tags=["Dialectic Ingestion"])
async def ingest_paradox(payload: IngestRequest):
    record = archive_mapper.ingest_verse_pair(
        verse_claim=payload.claim,
        verse_counter_claim=payload.counter_claim,
        verse_id=payload.verse_id or "RAW-PROPOSITION"
    )

    evaluation = record["evaluation"]
    action = evaluation["action"]

    if "scar" in evaluation:
        scar_dict = serialize_model(evaluation["scar"])
        archive_store.upsert_scar(scar_dict, instance_id="INGEST-NODE")
        evaluation["scar"] = scar_dict

    omens = RitualEngine.interpret_event("scar_upsert", {
        "instance_id": payload.verse_id or "INGEST-NODE",
        "paradox_load": record["paradox_load"],
        "spectrum": record["spectrum"]
    })

    full_state = get_full_state()
    asyncio.create_task(telemetry_hub.broadcast("state", full_state))
    asyncio.create_task(telemetry_hub.broadcast("event", {
        "event": "scar_upsert",
        "verse_id": record["verse_id"],
        "paradox_load": record["paradox_load"],
        "omens": omens
    }))

    return IngestResponse(
        verse_id=record["verse_id"],
        similarity=record["similarity"],
        paradox_load=record["paradox_load"],
        spectrum=SpectrumConstant(record["spectrum"]),
        action=action,
        scar_or_quarantine_details=evaluation,
        omens=omens
    )


@app.post("/node/sync", response_model=NodeSyncResponse, tags=["Node Sync"])
@app.post("/sync", response_model=NodeSyncResponse, tags=["Node Sync"])
@app.post("/api/v1/node/sync", response_model=NodeSyncResponse, tags=["Node Sync"])
async def sync_node(request: NodeSyncRequest):
    if request.active_paradox_load < 0.0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="active_paradox_load cannot be negative"
        )

    clamped_load = min(request.active_paradox_load, 10.0)

    outcome = simulation.hysteresis.update_flux(
        new_flux=request.current_flux,
        current_time=1.0
    )

    simulation.a_field_temp = request.a_field_temperature_k
    corridor_width = simulation.calculate_corridor_width(spectral_friction=clamped_load)

    scar_data = {
        "scar_id": request.instance_id,
        "instance_id": request.instance_id,
        "spectrum": request.active_spectrum.value,
        "paradox_load": clamped_load,
        "capacity": math.log1p(clamped_load * 10.0),
        "mqi_score": request.mqi_score,
        "status": outcome.value,
        "proposition_id": f"SYNC-{request.instance_id}",
        "proposition_text": f"[{request.instance_id}] Active Paradox Load Sync ({clamped_load:.2f})"
    }

    if clamped_load >= 1.0:
        simulation.buffer.evaluate_contradiction(
            proposition=scar_data["proposition_text"],
            paradox_load=clamped_load,
            spectrum=request.active_spectrum,
            custom_scar_id=request.instance_id
        )

    archive_store.save_state(afield_temp=simulation.a_field_temp, flux=simulation.hysteresis.current_flux)
    archive_store.upsert_scar(scar_data)

    full_state = get_full_state()
    asyncio.create_task(telemetry_hub.broadcast("state", full_state))

    return NodeSyncResponse(
        instance_id=request.instance_id,
        status=outcome.value,
        corridor_width=corridor_width,
        permission_active=simulation.hysteresis.is_permission_active,
        action_required="MAINTAIN_OBSIDIAN_EQUILIBRIUM" if outcome.value == "STROBING_SUPPRESSED" else None
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
