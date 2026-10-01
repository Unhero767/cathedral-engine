# cathedral_engine/app/logging/sanitizer.py

import re
from typing import Any, Dict, Set

SENSITIVE_KEYS: Set[str] = {
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

# Regex pattern to detect high-entropy secrets or base64-ish strings (e.g., keys, tokens >= 32 chars)
SECRET_PATTERN = re.compile(r"^[A-Za-z0-9_\-\/\+\=]{32,}$")


def _is_secret_value(val: Any) -> bool:
    if isinstance(val, str) and SECRET_PATTERN.match(val):
        return True
    return False


def sanitize_payload(payload: Dict[str, Any], allowlist: Set[str] | None = None) -> Dict[str, Any]:
    """
    Recursively sanitize payload dictionary:
    - If allowlist is provided, drop any key not in the allowlist.
    - Redact known sensitive keys.
    - Inspect string values for high-entropy secret patterns and redact them.
    """
    if not isinstance(payload, dict):
        return {}

    sanitized: Dict[str, Any] = {}

    for key, value in payload.items():
        key_lower = key.lower()

        if allowlist is not None and key_lower not in allowlist:
            continue

        if key_lower in SENSITIVE_KEYS or _is_secret_value(value):
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_payload(value, allowlist=allowlist)
        elif isinstance(value, list):
            sanitized[key] = f"[list length={len(value)}]"
        else:
            sanitized[key] = value

    return sanitized
