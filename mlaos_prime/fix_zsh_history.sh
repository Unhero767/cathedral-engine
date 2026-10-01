#!/usr/bin/env bash
# ====================================================================
# MLAOS-Prime :: Zsh History Expansion Disabler & Fixer
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
set -e

# Disable zsh history expansion (!) so pasted bash scripts don't trigger event not found errors
setopt +o banghist 2>/dev/null || true
echo "set +o banghist" >> ~/.zshrc

echo "==> [✓] Zsh history expansion disabled for cleaner terminal pasting."
