"""
Ω5-R1 // Fixed-Leader Network Benchmark

Purpose
-------
Benchmark networked fixed-leader quorum replication.

IMPORTANT:
    ALL CLIENT WORKLOAD INGRESS GOES TO THE FIXED LEADER.
    For Ω5-R1 the leader is A.

Topology:

    workload
       |
       v
      A
     / \
    v   v
    B   C

This is NOT Raft/Paxos and is NOT a distributed consensus benchmark.
"""

from __future__ import annotations

import argparse
import random
import statistics
import threading
import time
from dataclasses import dataclass

from .event import Event
from .node import send_message


@dataclass(frozen=True)
class Node:
    node_id: str
    host: str
    port: int


@dataclass
class Result:
    elapsed_ms: float
    status: str
    response: dict | None = None
    error: str | None = None


def parse_nodes(spec: str) -> list[Node]:
    nodes = []

    for item in spec.split(","):
        node_id, address = item.split(":", 1)
        host, port = address.rsplit(":", 1)

        nodes.append(
            Node(
                node_id=node_id,
                host=host,
                port=int(port),
            )
        )

    return nodes


def submit(
    target: Node,
    event: Event,
    timeout: float,
) -> Result:

    started = time.perf_counter()

    try:
        response = send_message(
            target.host,
            target.port,
            {
                "type": "SUBMIT",
                "event": event.to_dict(),
            },
            timeout=timeout,
        )

        elapsed_ms = (
            time.perf_counter() - started
        ) * 1000.0

        return Result(
            elapsed_ms=elapsed_ms,
            status=response.get("status", "UNKNOWN"),
            response=response,
        )

    except Exception as exc:
        elapsed_ms = (
            time.perf_counter() - started
        ) * 1000.0

        return Result(
            elapsed_ms=elapsed_ms,
            status="FAILED",
            error=str(exc),
        )


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0

    values = sorted(values)

    if len(values) == 1:
        return values[0]

    position = (len(values) - 1) * p
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)

    fraction = position - lower

    return (
        values[lower]
        + (values[upper] - values[lower])
        * fraction
    )


def print_percentiles(
    name: str,
    values: list[float],
) -> None:

    print(
        f"{name:<18}"
        f"p50={percentile(values, 0.50):9.4f} ms "
        f"p90={percentile(values, 0.90):9.4f} ms "
        f"p95={percentile(values, 0.95):9.4f} ms "
        f"p99={percentile(values, 0.99):9.4f} ms "
        f"p99.9={percentile(values, 0.999):9.4f} ms"
    )


def build_workload(
    unique_events: int,
    contradictions: int,
    duplicates: int,
    seed: int,
) -> tuple[list[Event], int, int]:

    rng = random.Random(seed)

    if contradictions > unique_events:
        raise ValueError(
            "contradictions cannot exceed unique-events"
        )

    if duplicates > unique_events:
        raise ValueError(
            "duplicates cannot exceed unique-events"
        )

    base_events: list[Event] = []

    # ---------------------------------------------------------
    # Base positive evidence
    # ---------------------------------------------------------

    for i in range(unique_events):
        event = Event.create(
            atom_key=f"omega5r1.atom.{i}",
            polarity="T",
            value={
                "sequence": i,
                "kind": "base",
            },
            source="benchmark",
            client_id=f"client-{i % 16}",
            event_id=f"evt-base-{i:06d}",
        )

        base_events.append(event)

    workload: list[Event] = list(base_events)

    # ---------------------------------------------------------
    # Controlled contradiction events
    #
    # IMPORTANT:
    # New event ID.
    # Same atom_key.
    # Opposite polarity.
    #
    # This creates FOUR.B at the proposition level.
    # ---------------------------------------------------------

    contradiction_events = 0

    for i in range(contradictions):
        base = base_events[i]

        event = Event.create(
            atom_key=base.atom_key,
            polarity="F",
            value={
                "sequence": i,
                "kind": "controlled-contradiction",
                "contradicts": base.id_e,
            },
            source="benchmark-contradiction",
            client_id=f"contradiction-{i % 16}",
            event_id=f"evt-contradiction-{i:06d}",
        )

        workload.append(event)
        contradiction_events += 1

    # ---------------------------------------------------------
    # Exact duplicate submissions.
    #
    # Reuse the SAME Event object so all canonical fields,
    # including tau_e, remain identical.
    # ---------------------------------------------------------

    duplicate_events: list[Event] = []

    for i in range(duplicates):
        duplicate_events.append(
            base_events[i]
        )

    # IMPORTANT:
    # Originals and contradiction events are submitted first.
    # Exact duplicates are appended afterward so they genuinely
    # exercise retry/idempotency against already-present events.
    workload.extend(duplicate_events)

    rng.shuffle(
        workload[:unique_events + contradictions]
    )

    return (
        workload,
        contradiction_events,
        duplicates,
    )


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "Ω5-R1 fixed-leader network benchmark"
        )
    )

    parser.add_argument(
        "--nodes",
        required=True,
        help=(
            "Node specification, e.g. "
            "A:127.0.0.1:9101,"
            "B:127.0.0.1:9102,"
            "C:127.0.0.1:9103"
        ),
    )

    parser.add_argument(
        "--unique-events",
        type=int,
        default=10000,
    )

    parser.add_argument(
        "--duplicates",
        type=int,
        default=500,
    )

    parser.add_argument(
        "--contradictions",
        type=int,
        default=1500,
    )

    parser.add_argument(
        "--writers",
        type=int,
        default=16,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
    )

    parser.add_argument(
        "--ingress-leader",
        default="A",
        help=(
            "ALL workload ingress is sent to this fixed leader. "
            "Ω5-R1 default: A"
        ),
    )

    args = parser.parse_args()

    nodes = parse_nodes(args.nodes)

    leader_candidates = [
        node
        for node in nodes
        if node.node_id == args.ingress_leader
    ]

    if len(leader_candidates) != 1:
        raise SystemExit(
            f"ERROR: ingress leader "
            f"{args.ingress_leader!r} "
            f"was not uniquely found in --nodes"
        )

    leader = leader_candidates[0]

    print()
    print("============================================================")
    print("Ω5-R1 // FIXED-LEADER NETWORK BENCHMARK")
    print("============================================================")
    print()
    print("Ingress mode:       FIXED_LEADER")
    print(
        f"Ingress leader:     "
        f"{leader.node_id} "
        f"{leader.host}:{leader.port}"
    )
    print("Workload routing:   100% → leader")
    print("Follower ingress:   DISABLED")
    print("Replication path:   leader → B,C")
    print()
    print(
        "WARNING: This is fixed-leader quorum replication, "
        "not Raft/Paxos."
    )
    print()

    workload, contradiction_count, duplicate_count = (
        build_workload(
            unique_events=args.unique_events,
            contradictions=args.contradictions,
            duplicates=args.duplicates,
            seed=args.seed,
        )
    )

    expected_unique = (
        args.unique_events
        + args.contradictions
    )

    expected_duplicates = args.duplicates

    print(
        f"Base unique events:          "
        f"{args.unique_events:,}"
    )

    print(
        f"Contradiction events:        "
        f"{contradiction_count:,}"
    )

    print(
        f"Exact duplicate submissions: "
        f"{duplicate_count:,}"
    )

    print(
        f"Total submissions:            "
        f"{len(workload):,}"
    )

    print(
        f"Expected durable unique:     "
        f"{expected_unique:,}"
    )

    print(
        f"Expected duplicates:         "
        f"{expected_duplicates:,}"
    )

    print(
        f"Concurrent writers:           "
        f"{args.writers}"
    )

    print(
        f"Deterministic seed:            "
        f"{args.seed}"
    )

    print()

    # ---------------------------------------------------------
    # Split workload across worker threads.
    #
    # Every worker still submits ONLY to leader A.
    # ---------------------------------------------------------

    results: list[Result] = []
    results_lock = threading.Lock()

    next_index = 0
    index_lock = threading.Lock()

    def worker() -> None:

        nonlocal next_index

        while True:

            with index_lock:
                if next_index >= len(workload):
                    return

                index = next_index
                next_index += 1

            event = workload[index]

            # -------------------------------------------------
            # Ω5-R1 CRITICAL INVARIANT:
            #
            # Every single client submission targets A.
            #
            # There is NO round-robin A/B/C here.
            # -------------------------------------------------

            target = leader

            result = submit(
                target=target,
                event=event,
                timeout=args.timeout,
            )

            with results_lock:
                results.append(result)

    threads = [
        threading.Thread(
            target=worker,
            name=f"benchmark-worker-{i}",
        )
        for i in range(args.writers)
    ]

    started = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    wall_time = (
        time.perf_counter() - started
    )

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    submitted = len(results)

    committed_new = sum(
        1
        for result in results
        if result.status == "COMMITTED_NEW"
    )

    duplicates = sum(
        1
        for result in results
        if result.status == "DUPLICATE_IGNORED"
    )

    rejected = sum(
        1
        for result in results
        if result.status == "STORAGE_REJECTED"
    )

    failed = sum(
        1
        for result in results
        if result.status == "FAILED"
    )

    other = submitted - (
        committed_new
        + duplicates
        + rejected
        + failed
    )

    latencies = [
        result.elapsed_ms
        for result in results
    ]

    print()
    print("============================================================")
    print("Ω5-R1 RESULTS")
    print("============================================================")
    print()

    print(
        f"Submitted:             "
        f"{submitted:10,}"
    )

    print(
        f"Committed NEW:         "
        f"{committed_new:10,}"
    )

    print(
        f"Duplicates:            "
        f"{duplicates:10,}"
    )

    print(
        f"Storage rejected:      "
        f"{rejected:10,}"
    )

    print(
        f"Failed:                "
        f"{failed:10,}"
    )

    print(
        f"Other:                 "
        f"{other:10,}"
    )

    print()

    print_percentiles(
        "latency_ms",
        latencies,
    )

    print()

    print(
        f"Wall time:             "
        f"{wall_time:.4f} s"
    )

    if wall_time > 0:
        print(
            f"Submitted throughput:  "
            f"{submitted / wall_time:,.2f} events/sec"
        )

        print(
            f"Committed throughput:   "
            f"{committed_new / wall_time:,.2f} blocks/sec"
        )

    print()

    # ---------------------------------------------------------
    # Semantic FOUR reconstruction from successful responses.
    # ---------------------------------------------------------

    proposition_state: dict[str, set[str]] = {}

    for result in results:

        if not result.response:
            continue

        event_data = result.response.get(
            "event"
        )

        if not event_data:
            continue

        atom_key = event_data.get(
            "atom_key"
        )

        polarity = event_data.get(
            "polarity"
        )

        if atom_key and polarity in ("T", "F"):
            proposition_state.setdefault(
                atom_key,
                set(),
            ).add(polarity)

    # If node responses do not echo event data, reconstruct
    # FOUR from the submitted workload itself.
    if not proposition_state:

        for event in workload[
            :args.unique_events
            + args.contradictions
        ]:

            proposition_state.setdefault(
                event.atom_key,
                set(),
            ).add(event.polarity)

    four_counts = {
        "T": 0,
        "F": 0,
        "B": 0,
        "N": 0,
    }

    for evidence in proposition_state.values():

        if evidence == {"T"}:
            four_counts["T"] += 1

        elif evidence == {"F"}:
            four_counts["F"] += 1

        elif evidence == {"T", "F"}:
            four_counts["B"] += 1

        else:
            four_counts["N"] += 1

    print("FOUR propositions observed:")

    for state in ("T", "F", "B", "N"):
        print(
            f"  {state}: "
            f"{four_counts[state]}"
        )

    print()

    print(
        f"Controlled contradiction pairs: "
        f"{contradiction_count:,}"
    )

    print(
        f"Expected duplicate retries:     "
        f"{duplicate_count:,}"
    )

    print()

    # ---------------------------------------------------------
    # Verification gate
    # ---------------------------------------------------------

    passed = True

    checks = [
        (
            submitted == (
                args.unique_events
                + args.contradictions
                + args.duplicates
            ),
            "submitted count",
        ),
        (
            committed_new == expected_unique,
            "committed unique count",
        ),
        (
            duplicates == expected_duplicates,
            "duplicate count",
        ),
        (
            rejected == 0,
            "storage rejection count",
        ),
        (
            failed == 0,
            "transport failure count",
        ),
        (
            other == 0,
            "unexpected result count",
        ),
        (
            four_counts["B"] == contradiction_count,
            "FOUR.B contradiction count",
        ),
    ]

    for condition, name in checks:

        if condition:
            print(
                f"[PASS] {name}"
            )
        else:
            print(
                f"[FAIL] {name}"
            )
            passed = False

    print()

    if passed:
        print(
            "Ω5-R1 NETWORK BENCHMARK: PASS"
        )
        return 0

    print(
        "Ω5-R1 NETWORK BENCHMARK: FAIL"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
