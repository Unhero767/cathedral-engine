#!/usr/bin/env bash
# ====================================================================
# MLAOS-Prime :: High-End IDE Language Servers Installation
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
set -e

echo "Installing language servers and tooling for C#, Python, and Godot..."

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew not detected."
    exit 1
fi

# Install Python pyright and node (for various LSPs)
brew install pyright node

# Install C# tools (.NET SDK if missing)
if ! command -v dotnet &> /dev/null; then
    brew install --cask dotnet-sdk
fi

echo "IDE toolchain dependencies installed successfully."
