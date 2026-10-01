#!/usr/bin/env bash
# ====================================================================
# MLAOS-Prime :: One-Shot Turnkey Test Runner
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
set -e

echo "==> [Σ-7] Initializing One-Shot Test Pipeline..."
if command -v studio &> /dev/null; then
    studio test
else
    python3 studio.py test
fi
echo "==> [✓] Test execution sequence completed."
