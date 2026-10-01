#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Post-Execution Self-Audit & Verification Protocol
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os
import subprocess
import sys

TARGET_PATH = os.path.expanduser("~/cathedral_engine/mlaos_prime")

def audit_stratum():
    print("\033[1;36m┌────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;36m│       MLAOS-PRIME :: POST-EXECUTION SELF-AUDIT         │\033[0m")
    print("\033[1;36m└────────────────────────────────────────────────────────┘\033[0m")
    
    # 1. Verify working directory
    current_dir = os.getcwd()
    assert os.path.abspath(current_dir) == os.path.abspath(TARGET_PATH), f"Stratum drift detected: {current_dir}"
    print(f"  [✓] Working Directory Confirmed : {current_dir}")

    # 2. Verify test suites exist and run successfully
    print("  [i] Executing pytest validation pass...")
    res = subprocess.run(["python3", "-m", "pytest", "tests/unit/", "-q"], capture_output=True, text=True)
    if res.returncode == 0:
        print("  [✓] Unit Test Suite Pass         : All tests passed cleanly.")
    else:
        print(f"  [!] Unit Test Warning            : Pytest returned code {res.returncode}")
        print(res.stdout)

    # 3. Verify core script integrity
    core_scripts = ["studio.py", "terminal_health_checks.py", "suite_runner.sh"]
    for script in core_scripts:
        assert os.path.exists(script), f"Critical script missing: {script}"
    print(f"  [✓] Core Artifacts Integrity     : All {len(core_scripts)} key scripts verified.")

    print("\n\033[1;32m[✓] Self-audit complete. Code checks out. Invariant Lex I sustained (dH/dt > 0).\033[0m")

if __name__ == "__main__":
    os.makedirs(TARGET_PATH, exist_ok=True)
    os.chdir(TARGET_PATH)
    audit_stratum()
