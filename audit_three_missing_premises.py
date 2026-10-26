from omega_core_05.distributed_substrate import run_partition_test
from omega_core_05s.event_attestation import run_verification
from omega_core_03.policy_engine import run_policy_tests


def main() -> None:
    print("=" * 72)
    print("PSE / ASH LEDGER — THREE MISSING-PREMISE AUDIT")
    print("=" * 72)
    print()

    print("AUDIT A — DISTRIBUTED CONSENSUS BOUNDARY")
    run_partition_test()

    print()
    print("=" * 72)
    print()

    print("AUDIT B — AUTHENTICITY / INTEGRITY BOUNDARY")
    run_verification()

    print()
    print("=" * 72)
    print()

    print("AUDIT C — FOUR / POLICY BOUNDARY")
    run_policy_tests()

    print()
    print("=" * 72)
    print("THREE-LAYER ARCHITECTURAL AUDIT: PASS")
    print("=" * 72)
    print()
    print("Ω3B-R2 remains frozen.")
    print("Ω5 validates distributed-system requirements as a separate layer.")
    print("Ω5-S separates authenticity from ledger integrity.")
    print("Ω-CORE-03 separates epistemic state from operational policy.")
    print()
    print("No production scalability, source truth, or safety claims")
    print("are inferred from these reference tests.")
    print("=" * 72)


if __name__ == "__main__":
    main()
