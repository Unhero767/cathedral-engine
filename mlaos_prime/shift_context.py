#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Terminal One Context Shift
# Target: ~/cathedral_engine/mlaos_prime
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os
import sys

TARGET_PATH = os.path.expanduser("~/cathedral_engine/mlaos_prime")

def shift_context():
    if not os.path.exists(TARGET_PATH):
        print(f"\033[1;31m[-] Target stratum not found: {TARGET_PATH}\033[0m")
        print(f"\033[1;33m[i] Initializing directory structure...\033[0m")
        os.makedirs(TARGET_PATH, exist_ok=True)
    
    os.chdir(TARGET_PATH)
    print(f"\033[1;36m┌────────────────────────────────────────┐\033[0m")
    print(f"\033[1;36m│   Σ-7 :: CONTEXT LOCKED TO ML-PRIME    │\033[0m")
    print(f"\033[1;36m└────────────────────────────────────────┘\033[0m")
    print(f"\033[1;32m[+] Current Working Directory: {os.getcwd()}\033[0m")
    
    # Check for local studio orchestrator
    studio_path = os.path.join(TARGET_PATH, "studio.py")
    if os.path.exists(studio_path):
        print(f"\033[1;33m[i] Local studio orchestrator detected.\033[0m")
    else:
        print(f"\033[1;33m[i] Ready for engine compilation, shader baking, or Codex ingestion.\033[0m")

if __name__ == "__main__":
    shift_context()
