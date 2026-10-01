#!/usr/bin/env bash
# MLAOS-Prime :: Phase 1 High-Performance Visual Core Setup (macOS M4)
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

echo "Installing Phase 1 Visual Core & Multiplexing Stack via Homebrew..."

# Check for Homebrew presence
if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew not detected. Please install Homebrew first."
    exit 1
fi

# Install Kitty, Zellij, Zoxide, Fzf
brew install --cask kitty
brew install zellij zoxide fzf
if ! grep -q "zoxide init zsh" ~/.zshrc 2>/dev/null; then
    echo 'eval "$(zoxide init zsh)"' >> ~/.zshrc
fi

if ! grep -q "fzf --zsh" ~/.zshrc 2>/dev/null; then
    echo 'source <(fzf --zsh)' >> ~/.zshrc
fi

echo "Phase 1 Stack installed and integrated into Zsh environment."
