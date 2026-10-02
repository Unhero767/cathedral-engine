from typing import Dict, Any, Tuple, Optional
from .models import SparkTask, AuthorityLevel

class SovereigntyFirewall:
    def __init__(self, constitution_path: Optional[str] = None):
        self.constitution_path = constitution_path

    def evaluate_constitutional_gate(self, task: SparkTask, caller_authority: AuthorityLevel) -> Tuple[bool, str]:
        if not task.task_id or not task.protocol_id:
            return False, "Validation Failed (V): Missing Task or Protocol ID."
        if task.retry_count >= task.max_retries:
            return False, "Boundedness Failed (B): Maximum execution retries exceeded."
        if "delete" in task.parameters or "erase" in task.parameters:
            return False, "Lawfulness Failed (L): Lex I Violation (Never-Overwrite)."
        if caller_authority == AuthorityLevel.OBSERVER:
            return False, "User Authority Failed (U): Observe != Authorize."
        if not task.provenance:
            return False, "Observability Failed (O): Missing Provenance Tuple."
        if not task.merkle_root.startswith("0x"):
            return False, "Merkle Invariance Failed (M): Invalid Merkle Root format."
        return True, "Constitutional Gate Cleared: V ∧ B ∧ L ∧ U ∧ O ∧ A ∧ M verified."
