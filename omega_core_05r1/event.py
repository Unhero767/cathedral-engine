"""
Ω5-R1 // Event Envelope

Canonical network event representation.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import time
import uuid


@dataclass(frozen=True)
class Event:
    id_e: str
    atom_key: str
    polarity: str
    value: object
    source: str
    tau_e: float
    client_id: str

    @staticmethod
    def create(
        atom_key: str,
        polarity: str,
        value: object,
        source: str,
        client_id: str,
        event_id: str | None = None,
    ) -> "Event":

        if polarity not in ("T", "F"):
            raise ValueError("polarity must be T or F")

        return Event(
            id_e=event_id or str(uuid.uuid4()),
            atom_key=atom_key,
            polarity=polarity,
            value=value,
            source=source,
            tau_e=time.time(),
            client_id=client_id,
        )

    def to_dict(self) -> dict:
        return {
            "id_e": self.id_e,
            "atom_key": self.atom_key,
            "polarity": self.polarity,
            "value": self.value,
            "source": self.source,
            "tau_e": self.tau_e,
            "client_id": self.client_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Event":
        return Event(
            id_e=data["id_e"],
            atom_key=data["atom_key"],
            polarity=data["polarity"],
            value=data["value"],
            source=data["source"],
            tau_e=float(data["tau_e"]),
            client_id=data["client_id"],
        )

    def canonical_bytes(self) -> bytes:
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def content_hash(self) -> str:
        return hashlib.sha256(
            self.canonical_bytes()
        ).hexdigest()
