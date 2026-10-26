"""
PSE Core integrated verification gate.

Runs each independently verified layer through its public CLI entry point.

Ω3-R2  -> semantic / ledger / DAG verification
Ω5     -> distributed failure / quorum model
Ω5-S   -> event authenticity / Ed25519 attestation
Ω-CORE-03 -> FOUR -> operational policy mapping

Important:
    This gate verifies the current reference implementations.
    It does not establish distributed production scalability,
    source truth, enterprise SLA, or production reliability.
"""

from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    (
        "Ω3-R2",
        [
            sys.executable,
            "-m",
            "omega_core_02.benchmark_omega3_suite",
            "--verify-only",
        ],
    ),
    (
        "Ω5",
        [
            sys.executable,
            "-m",
            "omega_core_05.distributed_substrate",
        ],
    ),
    (
        "Ω5-S",
        [
            sys.executable,
            "-m",
            "omega_core_05s.event_attestation",
        ],
    ),
    (
        "Ω-CORE-03",
        [
            sys.executable,
            "-m",
            "omega_core_03.policy_engine",
        ],
    ),
]


def run_gate(name: str, command: list[str]) -> bool:
    print(f"\n[{name}]")
    print("-" * 72)
    print("$", " ".join(command))

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name} (exit code {result.returncode})")
    return False


def main() -> int:
    print("=" * 72)
    print("PSE CORE // INTEGRATED VERIFICATION GATE")
    print("=" * 72)

    results = {}

    for name, command in COMMANDS:
        results[name] = run_gate(name, command)

    print("\n" + "=" * 72)
    print("INTEGRATED RESULT")
    print("=" * 72)

    failed = []

    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")

        if not passed:
            failed.append(name)

    print()

    if failed:
        print("INTEGRATED VERIFICATION: FAIL")
        print("Failed layers:")
        for name in failed:
            print(f"  - {name}")
        return 1

    print("INTEGRATED VERIFICATION: PASS")
    print()
    print("Verified boundary:")
    print("  evidence preservation")
    print("  FOUR contradiction semantics")
    print("  append-only lineage")
    print("  cryptographic integrity")
    print("  controlled DAG topology")
    print("  quorum/partition model")
    print("  event authenticity")
    print("  policy/action separation")
    print()
    print("NOT YET PROVEN:")
    print("  distributed multi-writer production scalability")
    print("  source truth")
    print("  networked consensus implementation")
    print("  multi-region durability")
    print("  enterprise SLA")
    print("  production operational reliability")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
