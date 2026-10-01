#!/usr/bin/env bash
# ====================================================================
# MLAOS-Prime :: Terminal Stack Installer & Verifier (Homebrew)
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
set -e

# Ensure we are in the correct stratum
cd ~/cathedral_engine/mlaos_prime

echo "==> [Σ-7] Checking and installing terminal stack components via Homebrew..."

# List of brew packages corresponding to our top 10 stack
PACKAGES=(kitty zellij neovim zoxide fzf lazygit bottom ripgrep fd dotnet)

for pkg in "${PACKAGES[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  [✓] $pkg is already installed."
    else
        echo "  [-] Installing $pkg..."
        brew install "$pkg" || echo "  [!] Warning: Could not install $pkg via brew (may require manual setup)."
    fi
done

echo "==> [✓] Terminal stack audit and installation check complete."
