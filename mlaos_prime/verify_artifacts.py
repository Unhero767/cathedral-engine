#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Artifact Integrity & Persistence Verification
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os

REQUIRED_ARTIFACTS = [
    "studio.py",
    "tests/unit/test_mlaos_core.py",
    "tests/unit/test_belnap_dunn.py",
    "tests/unit/test_terminal_bridge.py",
    "run_tests.sh",
    "scaffold_tests.sh",
    "fix_zsh_history.sh",
    "test_pipeline.sh",
    "expand_mlaos_tests.sh",
    "sovereign_status.py",
    "test_terminal_embedding.sh"
]

def check_artifacts():
    print("\033[1;36m┌────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;36m│       MLAOS-PRIME :: ARTIFACT VERIFICATION MATRIX      │\033[0m")
    print("\033[1;36m└────────────────────────────────────────────────────────┘\033[0m")
    
    missing = []
    for artifact in REQUIRED_ARTIFACTS:
        exists = os.path.exists(artifact)
        status = "\033[1;32m[VERIFIED]\033[0m" if exists else "\033[1;31m[MISSING]\033[0m"
        print(f"  {status} {artifact}")
        if not exists:
            missing.append(artifact)
            
    print("\n\033[1;33m[i] Checking global studio binary link (~/.local/bin/studio)...\033[0m" )
    global_studio = os.path.expanduser("~/.local/bin/studio")
    if os.path.exists(global_studio):
        print("  \033[1;32m[VERIFIED]\033[0m ~/.local/bin/studio is linked.")
    else:
        print("  \033[1;31m[MISSING]\033[0m Global studio link not found. Run 'cp studio.py ~/.local/bin/studio' and 'chmod +x ~/.local/bin/studio'.")

    if missing:
        print(f"\n\033[1;31m[-] Warning: {len(missing)} artifact(s) not found in current stratum.\033[0m")
    else:
        print("\n\033[1;32m[✓] All core scripts, test suites, and orchestrators are fully materialized and persisted.\033[0m")

if __name__ == "__main__":
    check_artifacts()
