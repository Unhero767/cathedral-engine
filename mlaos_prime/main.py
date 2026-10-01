# ====================================================================
# MLAOS-Prime :: FastAPI Sovereign Router & Arbiter
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os
import sqlite3
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import clr

# --- Paraconsistent C# Bindings ---
DLL_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 
    "CathedralEngine.Solvers/bin/Release/net10.0/CathedralEngine.Solvers.dll"
))

try:
    clr.AddReference(DLL_PATH)
    from CathedralEngine.Solvers import BelnapDunnMatrix, TruthValue
    CS_SOLVER_ACTIVE = True
except Exception as e:
    CS_SOLVER_ACTIVE = False
    print(f"[!] FRACTURE: CathedralEngine.Solvers.dll offline. {e}")

# --- Ash Archive SQLite Configuration ---
DB_PATH = "data/ash_archive/ledger.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_ledger():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                index_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                event_type TEXT,
                claim_a INTEGER,
                claim_b INTEGER,
                squeeze_angle REAL,
                scar_id TEXT
            )
        ''')
init_ledger()

# --- Sovereign Arbiter Intelligence ---
class SovereignArbiter:
    @staticmethod
    def gatekeeper(claim_a: int, claim_b: int, angle: float) -> dict:
        """
        Intelligence: When to inscribe vs. when to drop.
        """
        if angle >= 54.0:
            # Structurally significant. Write to DAG.
            scar_id = f"OBSIDIAN-{int(datetime.datetime.now().timestamp())}"
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO blocks (timestamp, event_type, claim_a, claim_b, squeeze_angle, scar_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (datetime.datetime.utcnow().isoformat(), "HARMONIC_SCAR", claim_a, claim_b, angle, scar_id)
                )
            return {
                "decision": "INSCRIBED_TO_ARCHIVE",
                "reasoning": "Dialetheic friction resolved into load-bearing structure.",
                "scar_id": scar_id
            }
        else:
            # Linear tautology. Drop from memory.
            return {
                "decision": "DROPPED_BY_ARBITER",
                "reasoning": "Linear tautology (dH/dt = 0). Adds zero value to the Cathedral.",
                "scar_id": "NONE"
            }

# --- FastAPI API Router ---
app = FastAPI(title="MLAOS-Prime Backend")

class ReasonRequest(BaseModel):
    claim_a: int  # 0=None, 1=False, 2=True, 3=Both
    claim_b: int

@app.post("/reason")
def reason_dialetheic(req: ReasonRequest):
    if not CS_SOLVER_ACTIVE:
        return {"error": "C# Solvers offline."}

    # 1. ALWAYS DO THE MATH
    val_a = TruthValue(req.claim_a)
    val_b = TruthValue(req.claim_b)
    
    conjunction = BelnapDunnMatrix.EvaluateConjunction(val_a, val_b)
    squeeze_angle = BelnapDunnMatrix.CalculateSqueezeAngle(val_a, val_b)

    # 2. APPLY INTELLIGENCE (When to inscribe vs when to drop)
    arbiter_verdict = SovereignArbiter.gatekeeper(req.claim_a, req.claim_b, squeeze_angle)

    return {
        "mathematical_evaluation": {
            "truth_meet_result": str(conjunction),
            "crystallization_angle": squeeze_angle
        },
        "arbiter_intelligence": arbiter_verdict
    }

@app.get("/ledger")
def get_ledger():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM blocks")
        total_scars = cursor.fetchone()[0]
    return {"status": "Ash Archive Mounted", "load_bearing_scars_inscribed": total_scars}

@app.get("/telemetry")
def get_telemetry():
    return {"datum": {"ego_density": "8.30"}, "nonary_vector": {"spectral_coherence": 0.98}}
