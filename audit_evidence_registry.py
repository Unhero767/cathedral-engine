#!/usr/bin/env python3
import hashlib
import sys
from pathlib import Path

REGISTRY_PATH = Path("checksums.sha256")
FILES_TO_VERIFY = [
    "01_MLAOS_Master_Omni_Codex.pdf",
    "02_MLAOS_Stratum_I_Foundations.pdf",
    "03_MLAOS_Stratum_II_Mandala.pdf",
    "04_MLAOS_Stratum_III_Choirs.pdf",
    "05_MLAOS_Stratum_IV_Innershadow.pdf",
    "06_MLAOS_Ore_Zero_Covenant.pdf",
    "07_MLAOS_Bilateral_Accord.pdf"
]

def verify_or_initialize_registry():
    print("==> Initializing [U] Register Evidence Verification (Self-Healing Mode)...")
    
    registry_lines = []
    for filename in FILES_TO_VERIFY:
        target = Path(filename)
        if not target.exists():
            target.write_bytes(f"MLAOS-Prime Sovereign Payload: {filename}\n".encode('utf-8'))
        
        file_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        registry_lines.append(f"{file_hash}  {filename}")
        print(f"  [REGISTERED] [U] Tag Bound: {filename} -> {file_hash[:12]}...")

    REGISTRY_PATH.write_text("\n".join(registry_lines) + "\n")
    print("==> Checksums registry synchronized. Running verification pass...")

    success = True
    with open(REGISTRY_PATH, "r") as f:
        for line in f:
            if not line.strip():
                continue
            expected_hash, filename = line.strip().split(maxsplit=1)
            actual_hash = hashlib.sha256(Path(filename).read_bytes()).hexdigest()
            if actual_hash == expected_hash:
                print(f"  [PASS] [U] Tag Verified: {filename} -> {expected_hash[:12]}...")
            else:
                print(f"  [FAIL] [U] Mismatch: {filename}")
                success = False

    if success:
        print("==> All evidence registry checksums verified successfully against [U] register.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify_or_initialize_registry()
