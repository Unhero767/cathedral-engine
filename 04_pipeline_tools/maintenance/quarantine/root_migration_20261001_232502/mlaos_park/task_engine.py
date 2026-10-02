import sqlite3
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from .models import SparkTask, TaskLifecycleState, AuthorityLevel
from .event_ledger import SparkEventLedger
from .sovereignty_gate import SovereigntyFirewall

class PersistentTaskEngine:
    def __init__(self, db_path: str, ledger: SparkEventLedger, gate: SovereigntyFirewall):
        self.db_path = db_path
        self.ledger = ledger
        self.gate = gate
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS spark_tasks (
                    task_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    protocol_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    parameters_json TEXT NOT NULL,
                    dependencies_json TEXT NOT NULL,
                    retry_count INTEGER NOT NULL DEFAULT 0,
                    max_retries INTEGER NOT NULL DEFAULT 3,
                    merkle_root TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)
            conn.commit()

    def create_task(self, task: SparkTask, caller_authority: AuthorityLevel = AuthorityLevel.OPERATIONAL) -> Dict[str, Any]:
        cleared, reason = self.gate.evaluate_constitutional_gate(task, caller_authority)
        if not cleared:
            return {"success": False, "error": f"Sovereignty Firewall Rejection: {reason}"}

        merkle_root = self.ledger.append_event(
            event_type="TASK_CREATED",
            aggregate_id=task.task_id,
            payload={"title": task.title, "protocol_id": task.protocol_id, "params": task.parameters}
        )
        task.merkle_root = merkle_root

        with self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO spark_tasks (task_id, title, protocol_id, state, parameters_json, dependencies_json, retry_count, max_retries, merkle_root, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id, task.title, task.protocol_id, task.state.value,
                json.dumps(task.parameters), json.dumps(task.dependencies),
                task.retry_count, task.max_retries, merkle_root, task.created_at, task.updated_at
            ))
            conn.commit()

        return {"success": True, "task_id": task.task_id, "state": task.state.value, "merkle_root": merkle_root}

    def transition_state(self, task_id: str, new_state: TaskLifecycleState, execution_entry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        ts = datetime.now(timezone.utc).isoformat()
        merkle_root = self.ledger.append_event(
            event_type=f"TASK_STATE_{new_state.value}",
            aggregate_id=task_id,
            payload={"new_state": new_state.value, "execution_data": execution_entry or {}}
        )

        with self._get_conn() as conn:
            conn.execute("UPDATE spark_tasks SET state = ?, merkle_root = ?, updated_at = ? WHERE task_id = ?",
                         (new_state.value, merkle_root, ts, task_id))
            conn.commit()

        return {"task_id": task_id, "new_state": new_state.value, "merkle_root": merkle_root, "timestamp": ts}
