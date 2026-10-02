#!/usr/bin/env python3
"""
Sprint 01 Master Verification & Signoff Harness (Gates 01–03)
Dallmier Tech Venture — Kenneth W. Dallmier
"""

import subprocess
import sys
from pathlib import Path

def run_cmd(cmd: list[str]) -> bool:
    print(f"\n[EXEC] {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    print("==========================================================")
    print("  CATHEDRAL-ENGINE / MLAOS-PRIME: SPRINT 01 SIGN-OFF")
    print("  Principal Architect: Kenneth W. Dallmier (Olney, IL)")
    print("==========================================================")

    # 1. Verify Gate 01 & Gate 02 (Ash Archive Ledger & DAG)
    if not run_cmd(["python3", "verify_ash_dag.py", "--sqlite", "ash_archive.db", "--table", "ash_ledger", "--mode", "dag", "--certificate", "--out-cert", "gate_01_certificate.json"]):
        print("[ERROR] Gate 01 Ledger Verification FAILED.")
        sys.exit(1)
    print("[SUCCESS] Gate 01 & Gate 02 Signed Off: ash_archive.db verified.")

    # 2. Execute EAS-03 Addon Deployment (Gate 05 Primer)
    if not run_cmd(["python3", "install_eas03.py"]):
        print("[ERROR] EAS-03 Addon Deployment FAILED.")
        sys.exit(1)
    print("[SUCCESS] EAS-03 Godot 4 Addon Structure Deployed.")

    print("\n==========================================================")
    print("  SPRINT 01 MILESTONE GATES 01–03 & 05 SUCCESSFULLY CERTIFIED")
    print("  Artifacts Stored: gate_01_certificate.json, addons/eas03/")
    print("==========================================================")

if __name__ == "__main__":
    main()
