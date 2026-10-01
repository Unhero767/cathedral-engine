#!/usr/bin/env bash
# MLAOS-Prime :: Comprehensive Suite Runner & Verification Hook
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

# Enforce correct working stratum
cd ~/cathedral_engine/mlaos_prime

echo "==> [Σ-7] Executing Full Terminal Suite Verification..."

# 1. Run health checks
python3 terminal_health_checks.py

# 2. Run pytest suite
echo "==> Running pytest suite..."
python3 -m pytest tests/unit/ -v

echo "==> [✓] All verification suites passed successfully. Invariant Lex I sustained."
