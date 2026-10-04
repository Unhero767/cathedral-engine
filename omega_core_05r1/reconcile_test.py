"""
Ω5-R1-R // Commit Reconciliation Test

Repairs follower PREPARED records whose corresponding event
is already COMMITTED on the fixed leader.

This is a recovery test, not a consensus test.
"""

from __future__ import annotations

from omega_core_05r1.node import send_message


NODES = [
    ("A", 9101),
    ("B", 9102),
    ("C", 9103),
]


def get_state(node: str, port: int) -> dict:

    response = send_message(
        "127.0.0.1",
        port,
        {"type": "STATE"},
        timeout=20.0,
    )

    if response.get("status") != "OK":
        raise RuntimeError(
            f"{node} STATE failed: {response}"
        )

    required = (
        "count",
        "committed_count",
        "prepared_count",
        "event_ids",
    )

    missing = [
        key
        for key in required
        if key not in response
    ]

    if missing:
        raise RuntimeError(
            f"{node} STATE missing fields: {missing}"
        )

    return response


def print_state(title: str):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    states = {}

    for node, port in NODES:

        state = get_state(node, port)

        states[node] = state

        print()
        print(f"[{node}]")
        print(
            f"  events:           "
            f"{state['count']}"
        )
        print(
            f"  committed:        "
            f"{state['committed_count']}"
        )
        print(
            f"  prepared:         "
            f"{state['prepared_count']}"
        )

    return states


def main():

    before = print_state(
        "Ω5-R1-R // STATE BEFORE RECONCILIATION"
    )

    print()
    print("=" * 60)
    print("Ω5-R1-R // RUN RECONCILIATION")
    print("=" * 60)

    response = send_message(
        "127.0.0.1",
        9101,
        {"type": "RECONCILE"},
        timeout=120.0,
    )

    print()
    print("Leader response:")
    print(response)

    if response.get("status") != "OK":

        raise SystemExit(
            "[FAIL] RECONCILE request failed"
        )

    if response.get("rejected", 0) != 0:

        print()
        print(
            "[FAIL] reconciliation reported "
            "rejected records"
        )

        raise SystemExit(1)

    after = print_state(
        "Ω5-R1-R // STATE AFTER RECONCILIATION"
    )

    print()
    print("=" * 60)
    print("Ω5-R1-R // VERIFICATION")
    print("=" * 60)

    passed = True

    counts = {
        node: state["count"]
        for node, state in after.items()
    }

    committed = {
        node: state["committed_count"]
        for node, state in after.items()
    }

    prepared = {
        node: state["prepared_count"]
        for node, state in after.items()
    }

    event_sets = {
        node: set(state["event_ids"])
        for node, state in after.items()
    }

    if len(set(counts.values())) == 1:
        print(
            "[PASS] event counts converge"
        )
    else:
        print(
            "[FAIL] event counts diverge"
        )
        passed = False

    if len(set(committed.values())) == 1:
        print(
            "[PASS] committed counts converge"
        )
    else:
        print(
            "[FAIL] committed counts diverge"
        )
        passed = False

    if all(
        value == 0
        for value in prepared.values()
    ):
        print(
            "[PASS] no PREPARED entries remain"
        )
    else:
        print(
            "[FAIL] PREPARED entries remain"
        )
        passed = False

    if (
        event_sets["A"]
        == event_sets["B"]
        == event_sets["C"]
    ):
        print(
            "[PASS] event-ID sets converge"
        )
    else:
        print(
            "[FAIL] event-ID sets diverge"
        )
        passed = False

    expected = 11500

    if all(
        value == expected
        for value in counts.values()
    ):
        print(
            f"[PASS] all nodes contain "
            f"{expected:,} events"
        )
    else:
        print(
            f"[FAIL] expected "
            f"{expected:,} events on all nodes"
        )
        passed = False

    if all(
        value == expected
        for value in committed.values()
    ):
        print(
            f"[PASS] all nodes have "
            f"{expected:,} committed events"
        )
    else:
        print(
            f"[FAIL] expected "
            f"{expected:,} committed events"
        )
        passed = False

    if passed:

        print()
        print(
            "Ω5-R1-R COMMIT RECONCILIATION: PASS"
        )

        return 0

    print()
    print(
        "Ω5-R1-R COMMIT RECONCILIATION: FAIL"
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
