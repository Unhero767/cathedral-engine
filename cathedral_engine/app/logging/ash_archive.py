# cathedral_engine/app/logging/ash_archive.py

import hashlib
from datetime import datetime
from typing import Optional

from fastapi import Request

from cathedral_engine.app.logging.constants import EventType
from cathedral_engine.app.logging.sanitizer import sanitize_payload
from cathedral_engine.app.telemetry.ledger import write_event


def _hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode("utf-8")).hexdigest()[:16]


async def log_auth_event(
    request: Request,
    *,
    status_code: int,
    event_type: EventType,
    error_code: Optional[str] = None,
    actor_user_id: Optional[str] = None,
    target_user_id: Optional[str] = None,
) -> None:
    """
    Emit a sanitized auth/audit event into the Ash Archive ledger using strict allowlists.
    """
    client_host = request.client.host if request.client else "unknown"
    client_ip_hash = _hash_ip(client_host)
    request_id = request.headers.get("x-request-id")

    try:
        body = await request.json()
    except Exception:
        body = {}

    safe_body = sanitize_payload(body, allowlist={"username"})

    event = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type.value,
        "actor_user_id": actor_user_id,
        "target_user_id": target_user_id,
        "client_ip_hash": client_ip_hash,
        "request_id": request_id,
        "status_code": status_code,
        "error_code": error_code,
        "metadata": {
            "method": request.method,
            "path": request.url.path,
            "body": safe_body,
            "user_agent": request.headers.get("user-agent"),
        },
    }

    await write_event(event)


async def log_iam_event(
    request: Request,
    *,
    status_code: int,
    event_type: EventType,
    actor_user_id: str,
    target_user_id: str,
    previous_role: str,
    new_role: str,
    error_code: Optional[str] = None,
) -> None:
    """
    Emit a sanitized IAM / role-change event into the Ash Archive ledger using strict allowlists.
    """
    client_host = request.client.host if request.client else "unknown"
    client_ip_hash = _hash_ip(client_host)
    request_id = request.headers.get("x-request-id")

    try:
        body = await request.json()
    except Exception:
        body = {}

    safe_body = sanitize_payload(body, allowlist={"new_role"})

    event = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type.value,
        "actor_user_id": actor_user_id,
        "target_user_id": target_user_id,
        "client_ip_hash": client_ip_hash,
        "request_id": request_id,
        "status_code": status_code,
        "error_code": error_code,
        "previous_role": previous_role,
        "new_role": new_role,
        "metadata": {
            "method": request.method,
            "path": request.url.path,
            "body": safe_body,
            "user_agent": request.headers.get("user-agent"),
        },
    }

    await write_event(event)
