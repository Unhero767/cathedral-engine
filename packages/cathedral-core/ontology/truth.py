from enum import Enum
from typing import Set, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class TruthValue(str, Enum):
    """
    Belnap-Dunn Four-Valued Logic Matrix:
    - TRUE: {1} (Accepted, not rejected)
    - FALSE: {0} (Rejected, not accepted)
    - BOTH: {1, 0} (Dialetheic contradiction: accepted and rejected)
    - NEITHER: {} (Gaps: neither accepted nor rejected)
    """
    TRUE = "TRUE"
    FALSE = "FALSE"
    BOTH = "BOTH"
    NEITHER = "NEITHER"

class ParaconsistentState(BaseModel):
    entity_id: str = Field(..., description="Canonical UUID or system identifier")
    truth: TruthValue = Field(..., description="Belnap-Dunn state coordinate")
    sources: List[str] = Field(default_factory=list, description="Contributing provenance nodes or simulation runs")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Epistemic confidence metric")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    harmonic_scar: Optional[str] = Field(None, description="Load-bearing contradiction marker if state is BOTH")

    class Config:
        frozen = True # Ensures immutable state representation across pipeline boundaries
