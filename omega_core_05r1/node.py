"""
Ω5-R1 // Hardened Networked Quorum Replication Node

A = fixed leader
B = follower
C = follower

This implementation provides:

    - TCP JSON-line transport
    - bounded inbound request concurrency
    - bounded outbound replication concurrency
    - SQLite WAL durability
    - prepared/committed lifecycle
    - quorum acknowledgement
    - idempotency by event ID + content hash
    - contradiction preservation
    - graceful client disconnect handling

IMPORTANT:

    This is NOT Raft.
    This is NOT Paxos.
    This is NOT distributed consensus.

It is a controlled fixed-leader quorum-replication
reference implementation.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import socket
import socketserver
import threading
import time

from .event import Event
from .storage import NodeStorage


NODES: dict[str, tuple[str, int]] = {}


# ============================================================
# Transport
# ============================================================

def send_message(
    host: str,
    port: int,
    message: dict,
    timeout: float = 15.0,
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

        sock.settimeout(timeout)

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


# ============================================================
# Replication state
# ============================================================

class ReplicationState:

    def __init__(
        self,
        node_id: str,
        peers: list[str],
        storage: NodeStorage,
    ):

        self.node_id = node_id
        self.peers = peers
        self.storage = storage

        self.lock = threading.RLock()

        self.next_index = (
            storage.max_log_index() + 1
        )

    def quorum_size(self) -> int:

        cluster_size = len(self.peers) + 1

        return (
            cluster_size // 2
            + 1
        )

    def allocate_index(self) -> int:

        with self.lock:

            index = self.next_index

            self.next_index += 1

            return index


# ============================================================
# Bounded TCP server
# ============================================================

class BoundedThreadingTCPServer(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer,
):

    allow_reuse_address = True
    daemon_threads = True

    request_queue_size = 128

    max_request_workers = 32

    def __init__(
        self,
        server_address,
        request_handler_class,
    ):

        self.request_slots = (
            threading.BoundedSemaphore(
                self.max_request_workers
            )
        )

        super().__init__(
            server_address,
            request_handler_class,
        )

    def process_request(
        self,
        request,
        client_address,
    ):

        acquired = (
            self.request_slots.acquire(
                timeout=15.0
            )
        )

        if not acquired:

            try:
                request.close()
            except Exception:
                pass

            return

        thread = threading.Thread(
            target=self._process_request_thread,
            args=(
                request,
                client_address,
            ),
            daemon=True,
        )

        thread.start()

    def _process_request_thread(
        self,
        request,
        client_address,
    ):

        try:

            self.finish_request(
                request,
                client_address,
            )

            self.shutdown_request(
                request
            )

        except Exception:

            try:
                self.handle_error(
                    request,
                    client_address,
                )
            except Exception:
                pass

        finally:

            self.request_slots.release()


# ============================================================
# TCP request handler
# ============================================================

class RequestHandler(
    socketserver.StreamRequestHandler
):

    def handle(self):

        self.connection.settimeout(
            20.0
        )

        try:

            line = self.rfile.readline()

            if not line:
                return

            request = json.loads(
                line.decode("utf-8")
            )

            response = (
                self.server.node.handle_request(
                    request
                )
            )

        except (
            BrokenPipeError,
            ConnectionResetError,
            ConnectionAbortedError,
            socket.timeout,
        ):

            return

        except Exception as exc:

            response = {
                "status": "ERROR",
                "error": str(exc),
            }

        try:

            payload = (
                json.dumps(
                    response,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            )

            self.wfile.write(
                payload.encode("utf-8")
            )

            self.wfile.flush()

        except (
            BrokenPipeError,
            ConnectionResetError,
            ConnectionAbortedError,
            socket.timeout,
            OSError,
        ):

            # Client disconnected before response
            # delivery. This is a transport condition,
            # not a semantic failure.
            return


# ============================================================
# Node
# ============================================================

class Node:

    def __init__(
        self,
        node_id: str,
        host: str,
        port: int,
        leader_id: str,
        peers: list[str],
        storage_path: str,
        replication_workers: int = 2,
    ):

        self.node_id = node_id
        self.host = host
        self.port = port
        self.leader_id = leader_id
        self.peers = peers

        self.storage = NodeStorage(
            storage_path
        )

        self.replication = (
            ReplicationState(
                node_id=node_id,
                peers=peers,
                storage=self.storage,
            )
        )

        # The Ω5-R1 reference implementation
        # deliberately serializes leader submissions.
        #
        # This prevents a high-concurrency client
        # workload from creating uncontrolled SQLite
        # and quorum contention.
        self.submit_lock = (
            threading.RLock()
        )

        # Small bounded replication pool.
        #
        # We deliberately do NOT create new threads
        # for every event.
        self.replication_pool = (
            concurrent.futures.ThreadPoolExecutor(
                max_workers=replication_workers,
                thread_name_prefix=(
                    f"{node_id}-replication"
                ),
            )
        )

    # --------------------------------------------------------
    # Request dispatch
    # --------------------------------------------------------

    def handle_request(
        self,
        request: dict,
    ) -> dict:

        request_type = request.get(
            "type"
        )

        if request_type == "PING":

            return {
                "status": "OK",
                "node_id": self.node_id,
            }

        if request_type == "SUBMIT":

            return self.handle_submit(
                request
            )

        if request_type == "REPLICATE":

            return self.handle_replicate(
                request
            )

        if request_type == "COMMIT":

            return self.handle_commit(
                request
            )

        if request_type == "STATE":

            return self.handle_state()

        if request_type == "RECONCILE":

            return self.handle_reconcile()

        if request_type == "REPLAY":

            return self.handle_replay()

        return {
            "status": "ERROR",
            "error": (
                f"unknown request type: "
                f"{request_type}"
            ),
        }

    # --------------------------------------------------------
    # Submit
    # --------------------------------------------------------

    def handle_submit(
        self,
        request: dict,
    ) -> dict:

        event = Event.from_dict(
            request["event"]
        )

        # Ω5-R1: A is the sole write leader.
        #
        # B/C forwarding is retained only as a
        # compatibility path. The benchmark should
        # submit directly to A.
        if self.node_id != self.leader_id:

            address = NODES[
                self.leader_id
            ]

            return send_message(
                address[0],
                address[1],
                request,
                timeout=20.0,
            )

        with self.submit_lock:

            return self._leader_submit(
                event
            )

    # --------------------------------------------------------
    # Leader submission
    # --------------------------------------------------------

    def _leader_submit(
        self,
        event: Event,
    ) -> dict:

        # ====================================================
        # 1. Idempotency / integrity
        # ====================================================

        existing = (
            self.storage.get_event(
                event.id_e
            )
        )

        if existing is not None:

            if (
                existing["content_hash"]
                == event.content_hash()
            ):

                return {
                    "status":
                        "DUPLICATE_IGNORED",
                    "id_e":
                        event.id_e,
                    "log_index":
                        existing["log_index"],
                    "committed":
                        bool(
                            existing["committed"]
                        ),
                }

            return {
                "status":
                    "STORAGE_REJECTED",
                "id_e":
                    event.id_e,
                "reason":
                    "same id_e with different "
                    "content hash",
            }

        # ====================================================
        # 2. Allocate leader log index
        # ====================================================

        log_index = (
            self.replication.allocate_index()
        )

        # ====================================================
        # 3. Local durable preparation
        # ====================================================

        local_status = (
            self.storage.append(
                log_index,
                event,
                committed=False,
            )
        )

        if local_status != "APPENDED_NEW":

            if (
                local_status
                == "DUPLICATE_IGNORED"
            ):

                existing = (
                    self.storage.get_event(
                        event.id_e
                    )
                )

                return {
                    "status":
                        "DUPLICATE_IGNORED",
                    "id_e":
                        event.id_e,
                    "log_index":
                        (
                            existing["log_index"]
                            if existing
                            else None
                        ),
                    "committed":
                        (
                            bool(
                                existing[
                                    "committed"
                                ]
                            )
                            if existing
                            else False
                        ),
                }

            return {
                "status":
                    "STORAGE_REJECTED",
                "id_e":
                    event.id_e,
            }

        # ====================================================
        # 4. Replicate to B/C
        # ====================================================

        acknowledgements = {
            self.node_id
        }

        futures = {}

        for peer_id in self.peers:

            future = (
                self.replication_pool.submit(
                    self._replicate_to_peer,
                    peer_id,
                    log_index,
                    event,
                )
            )

            futures[future] = peer_id

        deadline = (
            time.monotonic()
            + 20.0
        )

        pending = set(
            futures.keys()
        )

        while (
            pending
            and time.monotonic()
            < deadline
            and len(acknowledgements)
            < self.replication.quorum_size()
        ):

            remaining = max(
                0.001,
                deadline
                - time.monotonic(),
            )

            done, pending = (
                concurrent.futures.wait(
                    pending,
                    timeout=remaining,
                    return_when=(
                        concurrent.futures.FIRST_COMPLETED
                    ),
                )
            )

            for future in done:

                peer_id = futures[
                    future
                ]

                try:

                    success = (
                        future.result()
                    )

                except Exception:

                    success = False

                if success:

                    acknowledgements.add(
                        peer_id
                    )

        ack_list = sorted(
            acknowledgements
        )

        # ====================================================
        # 5. Quorum
        # ====================================================

        quorum_reached = (
            len(acknowledgements)
            >= self.replication.quorum_size()
        )

        if not quorum_reached:

            return {
                "status":
                    "QUORUM_UNAVAILABLE",
                "id_e":
                    event.id_e,
                "log_index":
                    log_index,
                "acks":
                    ack_list,
            }

        # ====================================================
        # 6. Commit leader
        # ====================================================

        commit_status = (
            self.storage.mark_committed(
                log_index
            )
        )

        if commit_status != "COMMITTED":

            return {
                "status":
                    "STORAGE_REJECTED",
                "id_e":
                    event.id_e,
                "log_index":
                    log_index,
                "reason":
                    "failed to mark leader "
                    "entry committed",
            }

        # ====================================================
        # 7. Commit followers
        # ====================================================

        for peer_id in ack_list:

            if peer_id == self.node_id:
                continue

            address = NODES[
                peer_id
            ]

            try:

                send_message(
                    address[0],
                    address[1],
                    {
                        "type":
                            "COMMIT",
                        "leader_id":
                            self.node_id,
                        "log_index":
                            log_index,
                        "id_e":
                            event.id_e,
                        "content_hash":
                            event.content_hash(),
                    },
                    timeout=20.0,
                )

            except (
                BrokenPipeError,
                ConnectionResetError,
                ConnectionAbortedError,
                socket.timeout,
                OSError,
            ):

                # Commit recovery/reconciliation is
                # outside Ω5-R1.
                pass

        return {
            "status":
                "COMMITTED_NEW",
            "id_e":
                event.id_e,
            "log_index":
                log_index,
            "acks":
                ack_list,
            "quorum":
                self.replication.quorum_size(),
        }

    # --------------------------------------------------------
    # Replication
    # --------------------------------------------------------

    def _replicate_to_peer(
        self,
        peer_id: str,
        log_index: int,
        event: Event,
    ) -> bool:

        address = NODES[
            peer_id
        ]

        try:

            response = send_message(
                address[0],
                address[1],
                {
                    "type":
                        "REPLICATE",
                    "leader_id":
                        self.node_id,
                    "log_index":
                        log_index,
                    "event":
                        event.to_dict(),
                },
                timeout=20.0,
            )

            status = response.get(
                "status"
            )

            if status == "APPENDED_NEW":

                return True

            if status == "DUPLICATE_IGNORED":

                return (
                    response.get(
                        "content_hash"
                    )
                    == event.content_hash()
                )

            return False

        except (
            BrokenPipeError,
            ConnectionResetError,
            ConnectionAbortedError,
            socket.timeout,
            OSError,
        ):

            return False

    # --------------------------------------------------------
    # Follower replication endpoint
    # --------------------------------------------------------

    def handle_replicate(
        self,
        request: dict,
    ) -> dict:

        if (
            request.get("leader_id")
            != self.leader_id
        ):

            return {
                "status":
                    "STORAGE_REJECTED",
                "reason":
                    "unexpected leader",
            }

        log_index = int(
            request["log_index"]
        )

        event = Event.from_dict(
            request["event"]
        )

        # Event-ID idempotency.
        existing = (
            self.storage.get_event(
                event.id_e
            )
        )

        if existing is not None:

            if (
                existing["content_hash"]
                == event.content_hash()
            ):

                return {
                    "status":
                        "DUPLICATE_IGNORED",
                    "id_e":
                        event.id_e,
                    "log_index":
                        existing[
                            "log_index"
                        ],
                    "content_hash":
                        existing[
                            "content_hash"
                        ],
                }

            return {
                "status":
                    "STORAGE_REJECTED",
                "reason":
                    "event id collision",
            }

        # Log-index integrity.
        existing_at_index = (
            self.storage.get_log_index(
                log_index
            )
        )

        if existing_at_index is not None:

            if (
                existing_at_index[
                    "content_hash"
                ]
                == event.content_hash()
            ):

                return {
                    "status":
                        "DUPLICATE_IGNORED",
                    "id_e":
                        event.id_e,
                    "log_index":
                        log_index,
                    "content_hash":
                        existing_at_index[
                            "content_hash"
                        ],
                }

            return {
                "status":
                    "STORAGE_REJECTED",
                "reason":
                    "log index collision",
            }

        status = (
            self.storage.append(
                log_index,
                event,
                committed=False,
            )
        )

        if status != "APPENDED_NEW":

            return {
                "status":
                    "STORAGE_REJECTED",
                "id_e":
                    event.id_e,
                "log_index":
                    log_index,
            }

        return {
            "status":
                "APPENDED_NEW",
            "node_id":
                self.node_id,
            "log_index":
                log_index,
            "id_e":
                event.id_e,
            "content_hash":
                event.content_hash(),
        }

    # --------------------------------------------------------
    # Commit
    # --------------------------------------------------------

    def handle_commit(
        self,
        request: dict,
    ) -> dict:

        log_index = int(
            request["log_index"]
        )

        event_id = request[
            "id_e"
        ]

        content_hash = request[
            "content_hash"
        ]

        existing = (
            self.storage.get_log_index(
                log_index
            )
        )

        if existing is None:

            return {
                "status":
                    "STORAGE_REJECTED",
                "reason":
                    "log index missing",
            }

        if existing["id_e"] != event_id:

            return {
                "status":
                    "STORAGE_REJECTED",
                "reason":
                    "event id mismatch",
            }

        if (
            existing["content_hash"]
            != content_hash
        ):

            return {
                "status":
                    "STORAGE_REJECTED",
                "reason":
                    "content hash mismatch",
            }

        status = (
            self.storage.mark_committed(
                log_index
            )
        )

        return {
            "status":
                status,
            "node_id":
                self.node_id,
            "log_index":
                log_index,
        }

    # --------------------------------------------------------
    # State
    # --------------------------------------------------------

    def handle_state(self) -> dict:

        return {
            "status":
                "OK",
            "node_id":
                self.node_id,
            "count":
                self.storage.count(),
            "committed_count":
                self.storage.committed_count(),
            "prepared_count":
                self.storage.prepared_count(),
            "event_ids":
                self.storage.event_ids(),
        }

    # --------------------------------------------------------
    # Reconciliation
    # --------------------------------------------------------

    def handle_reconcile(self) -> dict:

        # Ω5-R1-R:
        #
        # The leader is authoritative for the set of events that
        # reached its local COMMITTED state.
        #
        # Followers may contain durable PREPARED records whose
        # commit transition was not delivered during the original
        # submission.
        #
        # Reconciliation repairs those commit transitions.
        #
        # This is fixed-leader recovery logic.
        # It is NOT Raft/Paxos consensus.

        if self.node_id != self.leader_id:

            return {
                "status": "STORAGE_REJECTED",
                "node_id": self.node_id,
                "reason": "reconciliation must run on leader",
            }

        repaired = []
        already_committed = []
        rejected = []

        committed_events = (
            self.storage.replay(
                committed_only=True
            )
        )

        for record in committed_events:

            log_index = int(
                record["log_index"]
            )

            event_id = record["id_e"]

            content_hash = record[
                "content_hash"
            ]

            for peer_id in self.peers:

                address = NODES[peer_id]

                try:

                    response = send_message(
                        address[0],
                        address[1],
                        {
                            "type": "COMMIT",
                            "leader_id": self.node_id,
                            "log_index": log_index,
                            "id_e": event_id,
                            "content_hash": content_hash,
                        },
                        timeout=20.0,
                    )

                    status = response.get(
                        "status"
                    )

                    if status == "COMMITTED":

                        repaired.append(
                            {
                                "node_id": peer_id,
                                "log_index": log_index,
                            }
                        )

                    elif status == "ALREADY_COMMITTED":

                        already_committed.append(
                            {
                                "node_id": peer_id,
                                "log_index": log_index,
                            }
                        )

                    else:

                        rejected.append(
                            {
                                "node_id": peer_id,
                                "log_index": log_index,
                                "response": response,
                            }
                        )

                except Exception as exc:

                    rejected.append(
                        {
                            "node_id": peer_id,
                            "log_index": log_index,
                            "error": str(exc),
                        }
                    )

        return {
            "status": "OK",
            "node_id": self.node_id,
            "leader_committed_events": len(
                committed_events
            ),
            "repaired": len(repaired),
            "already_committed": len(
                already_committed
            ),
            "rejected": len(rejected),
            "repaired_records": repaired,
            "already_committed_records": (
                already_committed
            ),
            "rejected_records": rejected,
        }

    # --------------------------------------------------------
    # Replay
    # --------------------------------------------------------

    def handle_replay(self) -> dict:

        return {
            "status":
                "OK",
            "node_id":
                self.node_id,
            "events":
                self.storage.replay(
                    committed_only=True
                ),
        }

    # --------------------------------------------------------
    # Serve
    # --------------------------------------------------------

    def serve(self):

        server = (
            BoundedThreadingTCPServer(
                (
                    self.host,
                    self.port,
                ),
                RequestHandler,
            )
        )

        server.node = self

        print(
            f"[{self.node_id}] listening on "
            f"{self.host}:{self.port} "
            f"leader={self.leader_id} "
            f"replication_workers="
            f"{self.replication_pool._max_workers}"
        )

        try:

            server.serve_forever()

        finally:

            server.server_close()

            self.replication_pool.shutdown(
                wait=True
            )

            self.storage.close()


# ============================================================
# CLI
# ============================================================

def parse_nodes(
    spec: str,
) -> dict[str, tuple[str, int]]:

    result = {}

    for item in spec.split(","):

        node_id, host, port = (
            item.split(":")
        )

        result[node_id] = (
            host,
            int(port),
        )

    return result


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--node-id",
        required=True,
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
    )

    parser.add_argument(
        "--port",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--leader-id",
        default="A",
    )

    parser.add_argument(
        "--nodes",
        required=True,
        help=(
            "A:host:port,"
            "B:host:port,"
            "C:host:port"
        ),
    )

    parser.add_argument(
        "--storage",
        required=True,
    )

    parser.add_argument(
        "--replication-workers",
        type=int,
        default=2,
    )

    args = parser.parse_args()

    global NODES

    NODES = parse_nodes(
        args.nodes
    )

    peers = [
        node_id
        for node_id in NODES
        if node_id != args.node_id
    ]

    node = Node(
        node_id=args.node_id,
        host=args.host,
        port=args.port,
        leader_id=args.leader_id,
        peers=peers,
        storage_path=args.storage,
        replication_workers=(
            args.replication_workers
        ),
    )

    node.serve()


if __name__ == "__main__":
    main()
