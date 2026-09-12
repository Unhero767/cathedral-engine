import hashlib
import json
import uuid
from datetime import datetime, timezone

GENESIS_HASH = "0" * 64

def compute_state_hash(previous_hash: str, delta: dict) -> str:
    """Compute the new state hash from previous hash and delta."""
    payload = previous_hash + json.dumps(delta, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def create_event(
    entity_id: str,
    delta: dict,
    reason: str,
    author: str,
    authority: str,
    reality_tier: str,
    previous_hash: str,
    constitutional_ref: list = None,
    ai_provenance: dict = None
) -> dict:
    """Create a single immutable event."""
    event_id = str(uuid.uuid7())  # Requires uuid6 package or manual implementation
    timestamp = datetime.now(timezone.utc).isoformat()
    new_hash = compute_state_hash(previous_hash, delta)

    event = {
        "event_id": event_id,
        "timestamp": timestamp,
        "entity_id": entity_id,
        "previous_state_hash": previous_hash,
        "delta": json.dumps(delta, sort_keys=True),
        "new_state_hash": new_hash,
        "reason": reason,
        "author": author,
        "authority": authority,
        "reality_tier": reality_tier,
        "constitutional_ref": json.dumps(constitutional_ref or []),
        "ai_provenance": json.dumps(ai_provenance) if ai_provenance else None
    }
    return event

def verify_chain(events: list) -> bool:
    """Verify the integrity of the entire hash chain."""
    if not events:
        return True

    # First event must reference GENESIS_HASH
    if events[0]["previous_state_hash"] != GENESIS_HASH:
        return False

    for i in range(1, len(events)):
        if events[i]["previous_state_hash"] != events[i-1]["new_state_hash"]:
            return False

    return True