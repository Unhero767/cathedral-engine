"""
Ω5-R1 // Node-Local Durable Storage

SQLite provides node-local durability.

It is NOT the distributed consensus mechanism.

Each entry has an explicit lifecycle:

    PREPARED
        ↓
    COMMITTED

A PREPARED entry is durable but has not achieved quorum.

The semantic layer must never mistake durable preparation
for distributed commitment.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

from .event import Event


class NodeStorage:

    def __init__(
        self,
        path: str,
    ):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.conn = sqlite3.connect(
            str(self.path),
            check_same_thread=False,
        )

        self.conn.execute(
            "PRAGMA journal_mode=WAL"
        )

        self.conn.execute(
            "PRAGMA synchronous=FULL"
        )

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                log_index INTEGER PRIMARY KEY,
                id_e TEXT NOT NULL UNIQUE,
                atom_key TEXT NOT NULL,
                polarity TEXT NOT NULL,
                value_json TEXT NOT NULL,
                source TEXT NOT NULL,
                tau_e REAL NOT NULL,
                client_id TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                committed INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        self.conn.commit()

        self.lock = threading.RLock()

    # ---------------------------------------------------------
    # BASIC LOOKUPS
    # ---------------------------------------------------------

    def contains_event(
        self,
        event_id: str,
    ) -> bool:

        return (
            self.get_event(event_id)
            is not None
        )

    def get_event(
        self,
        event_id: str,
    ) -> dict | None:

        with self.lock:

            row = self.conn.execute(
                """
                SELECT
                    log_index,
                    id_e,
                    atom_key,
                    polarity,
                    value_json,
                    source,
                    tau_e,
                    client_id,
                    content_hash,
                    committed
                FROM events
                WHERE id_e = ?
                """,
                (event_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_dict(row)

    def get_log_index(
        self,
        log_index: int,
    ) -> dict | None:

        with self.lock:

            row = self.conn.execute(
                """
                SELECT
                    log_index,
                    id_e,
                    atom_key,
                    polarity,
                    value_json,
                    source,
                    tau_e,
                    client_id,
                    content_hash,
                    committed
                FROM events
                WHERE log_index = ?
                """,
                (log_index,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_dict(row)

    def max_log_index(self) -> int:

        with self.lock:

            row = self.conn.execute(
                """
                SELECT COALESCE(
                    MAX(log_index),
                    0
                )
                FROM events
                """
            ).fetchone()

        return int(row[0])

    # ---------------------------------------------------------
    # APPEND
    # ---------------------------------------------------------

    def append(
        self,
        log_index: int,
        event: Event,
        committed: bool = False,
    ) -> str:

        with self.lock:

            try:

                self.conn.execute(
                    """
                    INSERT INTO events (
                        log_index,
                        id_e,
                        atom_key,
                        polarity,
                        value_json,
                        source,
                        tau_e,
                        client_id,
                        content_hash,
                        committed
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?
                    )
                    """,
                    (
                        log_index,
                        event.id_e,
                        event.atom_key,
                        event.polarity,
                        json.dumps(
                            event.value,
                            sort_keys=True,
                            separators=(",", ":"),
                        ),
                        event.source,
                        event.tau_e,
                        event.client_id,
                        event.content_hash(),
                        int(committed),
                    ),
                )

                self.conn.commit()

                return "APPENDED_NEW"

            except sqlite3.IntegrityError:

                existing = (
                    self.get_event(
                        event.id_e
                    )
                )

                self.conn.rollback()

                if existing is not None:

                    if (
                        existing["content_hash"]
                        == event.content_hash()
                    ):
                        return (
                            "DUPLICATE_IGNORED"
                        )

                    return (
                        "STORAGE_REJECTED"
                    )

                existing_index = (
                    self.get_log_index(
                        log_index
                    )
                )

                if existing_index is not None:

                    return (
                        "STORAGE_REJECTED"
                    )

                return "STORAGE_REJECTED"

    # ---------------------------------------------------------
    # COMMIT
    # ---------------------------------------------------------

    def mark_committed(
        self,
        log_index: int,
    ) -> str:

        with self.lock:

            row = self.conn.execute(
                """
                SELECT committed
                FROM events
                WHERE log_index = ?
                """,
                (log_index,),
            ).fetchone()

            if row is None:
                return "STORAGE_REJECTED"

            if bool(row[0]):
                return "ALREADY_COMMITTED"

            self.conn.execute(
                """
                UPDATE events
                SET committed = 1
                WHERE log_index = ?
                """,
                (log_index,),
            )

            self.conn.commit()

            return "COMMITTED"

    # ---------------------------------------------------------
    # COUNTS
    # ---------------------------------------------------------

    def count(self) -> int:

        with self.lock:

            row = self.conn.execute(
                "SELECT COUNT(*) FROM events"
            ).fetchone()

        return int(row[0])

    def committed_count(self) -> int:

        with self.lock:

            row = self.conn.execute(
                """
                SELECT COUNT(*)
                FROM events
                WHERE committed = 1
                """
            ).fetchone()

        return int(row[0])

    def prepared_count(self) -> int:

        with self.lock:

            row = self.conn.execute(
                """
                SELECT COUNT(*)
                FROM events
                WHERE committed = 0
                """
            ).fetchone()

        return int(row[0])

    # ---------------------------------------------------------
    # EVENT IDS
    # ---------------------------------------------------------

    def event_ids(
        self,
        committed_only: bool = False,
    ) -> list[str]:

        query = """
            SELECT id_e
            FROM events
        """

        if committed_only:
            query += """
                WHERE committed = 1
            """

        query += """
            ORDER BY log_index
        """

        with self.lock:

            rows = self.conn.execute(
                query
            ).fetchall()

        return [
            row[0]
            for row in rows
        ]

    # ---------------------------------------------------------
    # REPLAY
    # ---------------------------------------------------------

    def replay(
        self,
        committed_only: bool = False,
    ) -> list[dict]:

        query = """
            SELECT
                log_index,
                id_e,
                atom_key,
                polarity,
                value_json,
                source,
                tau_e,
                client_id,
                content_hash,
                committed
            FROM events
        """

        if committed_only:
            query += """
                WHERE committed = 1
            """

        query += """
            ORDER BY log_index
        """

        with self.lock:

            rows = self.conn.execute(
                query
            ).fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    # ---------------------------------------------------------
    # INTERNAL
    # ---------------------------------------------------------

    @staticmethod
    def _row_to_dict(
        row,
    ) -> dict:

        return {
            "log_index": row[0],
            "id_e": row[1],
            "atom_key": row[2],
            "polarity": row[3],
            "value": json.loads(row[4]),
            "source": row[5],
            "tau_e": row[6],
            "client_id": row[7],
            "content_hash": row[8],
            "committed": bool(row[9]),
        }

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def close(self) -> None:

        with self.lock:
            self.conn.close()
