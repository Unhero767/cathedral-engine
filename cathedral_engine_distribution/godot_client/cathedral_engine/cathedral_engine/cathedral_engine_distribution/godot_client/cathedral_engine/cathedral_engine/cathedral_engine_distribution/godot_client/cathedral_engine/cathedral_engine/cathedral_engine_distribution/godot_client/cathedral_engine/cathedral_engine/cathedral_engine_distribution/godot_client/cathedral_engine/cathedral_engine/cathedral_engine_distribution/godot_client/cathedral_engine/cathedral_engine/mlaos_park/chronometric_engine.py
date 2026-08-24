from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from .models import ChronometricTrigger

class ChronometricTriggerEngine:
    def __init__(self):
        self.triggers: Dict[str, ChronometricTrigger] = {}
        self.register_trigger(ChronometricTrigger(
            trigger_id="TRIG_DAILY_437_PULSE",
            task_template_id="PROTO_CARRIER_CALIBRATE",
            temporal_expression="0 9 * * *",
            harmonic_carrier_hz=43.7
        ))

    def register_trigger(self, trigger: ChronometricTrigger):
        self.triggers[trigger.trigger_id] = trigger

    def evaluate_triggers(self, current_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        if current_time is None:
            current_time = datetime.now(timezone.utc)
        due = []
        for t_id, trigger in self.triggers.items():
            if trigger.is_active:
                due.append({
                    "trigger_id": t_id,
                    "task_template_id": trigger.task_template_id,
                    "carrier_frequency": trigger.harmonic_carrier_hz,
                    "evaluated_at": current_time.isoformat()
                })
        return due
