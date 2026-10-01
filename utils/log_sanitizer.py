# utils/log_sanitizer.py

from typing import Any, Dict

SENSITIVE_KEYS = {
    "password",
    "pass",
    "secret",
    "token",
    "authorization",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
}


def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively sanitize a payload dictionary:
    - Replace values of known sensitive keys with '[REDACTED]'
    - Recursively sanitize nested dictionaries
    - Truncate or summarize lists to avoid massive log blobs
    """
    if not isinstance(payload, dict):
        return {}

    sanitized = {}

    for key, value in payload.items():
        key_lower = key.lower()

        if key_lower in SENSITIVE_KEYS:
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_payload(value)
        elif isinstance(value, list):
            sanitized[key] = f"[list length={len(value)}]"
        else:
            sanitized[key] = value

    return sanitized
