"""
Ω5-R1 // TCP JSON-Line Transport
"""

from __future__ import annotations

import json
import socket


def send_message(
    host: str,
    port: int,
    message: dict,
    timeout: float = 5.0,
) -> dict:

    payload = (
        json.dumps(
            message,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )

    with socket.create_connection(
        (host, port),
        timeout=timeout,
    ) as sock:

        sock.sendall(payload)

        buffer = b""

        while b"\n" not in buffer:

            chunk = sock.recv(65536)

            if not chunk:
                break

            buffer += chunk

    if not buffer:
        raise RuntimeError(
            "remote node returned no response"
        )

    return json.loads(
        buffer.split(
            b"\n",
            1,
        )[0].decode("utf-8")
    )
