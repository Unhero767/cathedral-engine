import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class TaskLifecycleState(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    FAILED_QUARANTINED = "FAILED_QUARANTINED"
    EXILED = "EXILED"

class AuthorityLevel(str, enum.Enum):
    OBSERVER = "OBSERVER"
    OPERATIONAL = "OPERATIONAL"
    SOVEREIGN_ROOT = "SOVEREIGN"

@dataclass
class ProvenanceTuple:
    source_uri: str
    inscribed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    merkle_hash: str = "0x0000000000000000"
    confidence_interval: float = 1.0
    authority_level: AuthorityLevel = AuthorityLevel.OBSERVER

@dataclass
class SparkTask:
    task_id: str
    title: str
    protocol_id: str
    parameters: Dict[str, Any]
    state: TaskLifecycleState = TaskLifecycleState.PENDING
    dependencies: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    retry_count: int = 0
    max_retries: int = 3
    provenance: Optional[ProvenanceTuple] = None
    execution_log: List[Dict[str, Any]] = field(default_factory=list)
    merkle_root: str = "0x0000"

@dataclass
class ChronometricTrigger:
    trigger_id: str
    task_template_id: str
    temporal_expression: str
    harmonic_carrier_hz: float = 43.7
    is_active: bool = True
    last_pulsed_at: Optional[str] = None
    next_pulse_at: Optional[str] = None

@dataclass
class SparkProtocol:
    protocol_id: str
    version: str
    title: str
    description: str
    required_authority: AuthorityLevel
    execution_steps: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    signature_hash: str = "0x0000"

@dataclass
class ContextNode:
    node_id: str
    node_type: str
    uri: str
    content_hash: str
    provenance: ProvenanceTuple
    edges: List[str] = field(default_factory=list)
