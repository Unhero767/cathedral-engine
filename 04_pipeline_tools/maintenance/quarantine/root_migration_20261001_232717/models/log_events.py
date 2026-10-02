from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AuthLogEvent(BaseModel):
    ts: datetime
    event_type: str
    user_id: Optional[str] = None
    client_ip_hash: Optional[str] = None
    request_id: Optional[str] = None
    status_code: int
    error_code: Optional[str] = None
    metadata: dict
