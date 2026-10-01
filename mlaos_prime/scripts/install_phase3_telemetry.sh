#!/usr/bin/env bash
# MLAOS-Prime :: Phase 3 Advanced Visual Git & Telemetry Setup
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

echo "Installing LazyGit and Bottom (btm) via Homebrew..."

if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew not detected."
    exit 1
fi

brew install lazygit bottom

echo "Phase 3 Visual Git and Telemetry tools successfully installed."
