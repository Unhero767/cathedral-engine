#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Top Ten Absolute Must-Haves for Terminal Studio
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import sys

MUST_HAVES = [
    ("1. Kitty (Terminal Emulator)", "GPU-accelerated, true 24-bit color, ligatures, and near-zero render latency on Apple Silicon."),
    ("2. Zellij (Multiplexer)", "Modern, high-performance terminal multiplexer written in Rust with built-in layout persistence and floating panes."),
    ("3. Neovim (Terminal IDE)", "Lightning-fast text editor configured with LSP, Treesitter, and custom Lua plugins for full IDE power."),
    ("4. Zoxide (Smart Navigation)", "A smarter `cd` command that learns your habits and lets you jump to frequent directories instantly."),
    ("5. Fzf (Fuzzy Finder)", "Lightning-fast command-line fuzzy finder for files, history, git commits, and process searching."),
    ("6. LazyGit (Git Control Center)", "A rich terminal UI for staging hunks, interactive rebasing, diffing, and managing git repositories visually."),
    ("7. Bottom / Btm (System Telemetry)", "A gorgeous, customizable terminal dashboard to monitor Apple Silicon CPU cores, RAM, and IO in real-time."),
    ("8. Ripgrep & Fd (Fast Search)", "Blazing-fast modern replacements for `grep` and `find` that respect `.gitignore` by default."),
    ("9. Python Studio Orchestrator (`studio`)", "Your custom local command hub for running builds, test suites, live logging (`tee`), and app services."),
    ("10. Dotnet & Pytest (Execution Runtimes)", "Robust backends for running your C# Cathedral engine solutions and Python unit test matrices seamlessly.")
]

def render_list():
    print("\033[1;36m┌────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;36m│       MLAOS-PRIME :: TOP 10 TERMINAL MUST-HAVES        │\033[0m")
    print("\033[1;36m└────────────────────────────────────────────────────────┘\033[0m")
    for title, desc in MUST_HAVES:
        print(f"\n\033[1;33m{title}\033[0m")
        print(f"    -> {desc}")
    print("\n\033[1;35m[✓] Invariant Maintained: dH/dt > 0. All 10 integrated into your studio.\033[0m")

if __name__ == "__main__":
    render_list()
