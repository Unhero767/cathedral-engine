"""
server.py - FastAPI Sovereign Bridge for MLAOS-Prime & Godot Console
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import MLAOSCognitiveEngine
from codex import CodexEngine
from axioms import FourValuedLogic

app = FastAPI(title="MLAOS-Prime Sovereign Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MLAOSCognitiveEngine()

class PromptRequest(BaseModel):
    prompt: str

class ReasonRequest(BaseModel):
    claim_a: str
    claim_b: str

class ReduceRequest(BaseModel):
    goal: str

@app.post("/ask")
def ask_endpoint(req: PromptRequest):
    return engine.process_query(req.prompt)

@app.get("/telemetry")
def telemetry_endpoint():
    return engine.telemetry.capture_telemetry()

@app.get("/ledger")
def ledger_endpoint():
    last = engine.ledger.get_last_block()
    if not last:
        raise HTTPException(status_code=404, detail="Ash Archive ledger is empty.")
    return last

@app.get("/ledger/verify")
def ledger_verify_endpoint():
    valid = engine.ledger.verify_integrity()
    return {"merkle_dag_integrity_valid": valid}

@app.get("/codex/{term}")
def codex_endpoint(term: str):
    return CodexEngine.query(term)

@app.post("/reduce")
def reduce_endpoint(req: ReduceRequest):
    return engine.lex_v_reduction(req.goal)

@app.post("/reason")
def reason_endpoint(req: ReasonRequest):
    return engine.reasoner.evaluate_pair(
        req.claim_a, req.claim_b, FourValuedLogic.TRUE, FourValuedLogic.TRUE
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
