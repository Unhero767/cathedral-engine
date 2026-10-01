#!/usr/bin/env bash
# MLAOS-Prime :: Comprehensive Test & Studio Verification Suite
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

echo "==> [Σ-7] Running studio test harness..."
if command -v studio &> /dev/null; then
    studio test
else
    python3 studio.py test
fi

echo "==> [✓] Pipeline verification complete. Invariant Lex I sustained."
