import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from src.persistence import EVENT_LOG_PATH

class EventLogger:
    def __init__(self, log_path: Path = EVENT_LOG_PATH):
        self.log_path = log_path

    def append_event(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        event_record = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": event_type,
            "data": data
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_record) + "\n")
        return event_record

    def get_recent_events(self, limit: int = 50) -> list:
        if not self.log_path.exists():
            return []
        events = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        return events[-limit:]
