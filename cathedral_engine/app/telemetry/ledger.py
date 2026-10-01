# cathedral_engine/app/telemetry/ledger.py

import hashlib
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("ash_archive.ledger")

# In-memory tip pointer for the active hash chain (in production, persist this to the DB tip)
_LAST_BLOCK_HASH: Optional[str] = "0" * 64


def _compute_block_hash(prev_hash: str, event_data: Dict[str, Any]) -> str:
    """Compute SHA-256 hash chaining the previous block's hash with current event payload."""
    canonical_payload = json.dumps(event_data, sort_keys=True)
    hasher = hashlib.sha256()
    hasher.update(prev_hash.encode("utf-8"))
    hasher.update(canonical_payload.encode("utf-8"))
    return hasher.hexdigest()


async def write_event(event: dict) -> Dict[str, Any]:
    """
    Append an immutable event block to the Ash Archive ledger 
    backed by a cryptographic hash chain (prev_hash -> block_hash).
    """
    global _LAST_BLOCK_HASH

    # Bind current event to the cryptographic chain
    block_hash = _compute_block_hash(_LAST_BLOCK_HASH or ("0" * 64), event)
    
    chained_block = {
        "prev_hash": _LAST_BLOCK_HASH,
        "block_hash": block_hash,
        "event": event,
    }

    # Advance the chain tip
    _LAST_BLOCK_HASH = block_hash

    serialized = json.dumps(chained_block)
    logger.info("ASH_ARCHIVE_CHAIN_COMMITTED: %s", serialized)
    return chained_block
