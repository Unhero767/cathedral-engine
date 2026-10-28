#!/usr/bin/env python3
"""
MLAOS-Prime / Cathedral-Engine: Gate 3 FastAPI Sovereign Router & Manifold Broadcaster
Binds Book XXII ParaconsistentStratumValidator to Uvicorn (127.0.0.1:8765) and /ws/manifold.
"""

import sqlite3
import time
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Response, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

from tests.verify_n_t_b_dossier import ParaconsistentStratumValidator

router = APIRouter()
validator = ParaconsistentStratumValidator(db_path="ash_archive_stratum.db")


class InscribeRequest(BaseModel):
    stratum_id: str = Field(..., examples=["vault.axiom.042"])
    proposition: str = Field(..., examples=["P"])
    polarity: int = Field(..., description="+1 for affirmative, -1 for negation")
    sig: str = Field(..., examples=["0x9a8f..."])
    tx_id: Optional[str] = None
    timestamp_block: Optional[int] = None


class ManifoldConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_state(self, payload: dict):
        dead_sockets = []
        for connection in self.active_connections:
            try:
                await connection.send_json(payload)
            except Exception:
                dead_sockets.append(connection)
        for d in dead_sockets:
            self.disconnect(d)


manifold_bus = ManifoldConnectionManager()


@router.get("/v1/ash-archive/stratum/{stratum_id}")
async def get_stratum_state(stratum_id: str, response: Response):
    state, truth_vec, chain = validator.evaluate_stratum(stratum_id)
    response.headers["X-Commit-SHA"] = "8f4e2a9c"
    return validator._build_dossier_payload(
        stratum_id=stratum_id,
        transition=None,
        state=state,
        truth_vec=truth_vec,
        chain=chain
    )


@router.post("/v1/cathedral/inscribe")
async def inscribe_proposition(req: InscribeRequest, response: Response):
    t0 = time.perf_counter()
    if req.polarity not in (1, -1):
        raise HTTPException(status_code=400, detail="Polarity must be +1 or -1")

    pol_str = "+1" if req.polarity == 1 else "-1"
    tx_id = req.tx_id or f"tx_{int(time.time() * 1000000)}"
    ts_block = req.timestamp_block or int(time.time())

    try:
        payload = validator.inscribe(
            stratum_id=req.stratum_id,
            proposition=req.proposition,
            tx_id=tx_id,
            polarity=pol_str,
            timestamp_block=ts_block,
            sig=req.sig
        )
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=409, detail=f"Lex I Integrity Fault: {exc}")

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    response.headers["X-Commit-SHA"] = "8f4e2a9c"
    response.headers["X-Latency-Ms"] = f"{elapsed_ms:.3f}"

    if payload["epistemic_state"] == "B":
        response.status_code = status.HTTP_202_ACCEPTED
    else:
        response.status_code = status.HTTP_201_CREATED

    await manifold_bus.broadcast_state({
        "event": "STRATUM_TRANSITION",
        "latency_ms": round(elapsed_ms, 3),
        "dossier": payload
    })

    return payload


@router.websocket("/ws/manifold")
async def manifold_websocket_endpoint(websocket: WebSocket):
    await manifold_bus.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        manifold_bus.disconnect(websocket)
