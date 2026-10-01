# cathedral_engine/app/logging/constants.py

from enum import Enum


class EventType(str, Enum):
    AUTH_LOGIN_SUCCEEDED = "auth.login.succeeded"
    AUTH_LOGIN_FAILED = "auth.login.failed"
    IAM_ROLE_UPDATED = "iam.role.updated"
    PASSWORD_RESET_REQUESTED = "auth.password_reset.requested"
    CONFIG_CHANGED = "system.config.changed"
