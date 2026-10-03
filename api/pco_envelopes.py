"""
Cathedral-Engine: Gate 3
ProofCarryingObject envelopes (x*) enforcing explicit epistemic register tags:
(E, M, I, H, S, N) on all serializable payloads.
"""
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict, Optional
import time

class EpistemicRegisterTag(str, Enum):
    EMPIRICAL = "E"
    MODEL = "M"
    INTERPRETATION = "I"
    HYPOTHESIS = "H"
    SCAR = "S"
    NULL = "N"

class ProvenanceModel(BaseModel):
    source: str
    tau: float = Field(default_factory=time.time)
    tick: int
    actor: str
    signature: str
    context: str
    latency_delta: float

class ProofCarryingObjectResponse(BaseModel):
    """
    Formal envelope: x* = (x, pi, lambda, epsilon, rho)
    """
    value: Any
    provenance: ProvenanceModel
    merkle_lineage: str
    epistemic_register: EpistemicRegisterTag
    uncertainty_metadata: Dict[str, Any]

    @field_validator("epistemic_register")
    @classmethod
    def validate_register_classification(cls, v: EpistemicRegisterTag) -> EpistemicRegisterTag:
        if v not in EpistemicRegisterTag:
            raise ValueError(f"Unregistered epistemic status: {v}")
        return v
