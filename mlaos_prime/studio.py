#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Unified Studio Execution, Testing & Logging Engine
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import sys
import subprocess
import os
import datetime

TASKS = {
    "init": "Scaffolding workspace structural directories...",
    "build": "dotnet build CathedralEngine.sln -c Release",
    "test": "pytest tests/unit/ -v",
    "test-watch": "ptw --ext=.py,.cs tests/unit/",
    "run-api": "uvicorn main:app --reload --host 127.0.0.1 --port 8000",
    "run-engine": "godot --path .",
    "clean": "rm -rf ./builds/* ./logs/* .pytest_cache",
    "monitor": "btm",
    "git": "lazygit"
}

def render_banner():
    print("\033[1;36m┌────────────────────────────────────────┐\033[0m")
    print("\033[1;36m│     CATHEDRAL STUDIO LOGGING CORE      │\033[0m")
    print("\033[1;36m└────────────────────────────────────────┘\033[0m")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TASKS:
        render_banner()
        print("Usage: studio [command]\n\nAvailable Commands:")
        for cmd, desc in TASKS.items():
            print(f"  \033[1;32m{cmd:<12}\033[0m : {desc}")
        sys.exit(1)

    action = sys.argv[1]

    if action == "init":
        os.makedirs("builds", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        print("\033[1;32m[+] Studio structural directories initialized successfully.\033[0m")
        return

    command_str = TASKS[action]
    
    # Skip logging redirection for interactive TUI tools (btm, lazygit)
    if action in ["monitor", "git"]:
        print(f"\033[1;33m==> Launching interactive TUI: {command_str}\033[0m")
        result = subprocess.run(command_str, shell=True)
        sys.exit(result.returncode)

    # Prepare log file path for non-interactive commands (build, test, run-api, etc.)
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/{action}_{timestamp}.log"

    print(f"\033[1;33m==> Executing: {command_str}\033[0m")
    print(f"\033[1;35m[i] Output mirroring to: {log_filename}\033[0m")

    # Use 'tee' via shell to pipe stdout/stderr to both console and log file simultaneously
    tee_command = f"{command_str} 2>&1 | tee {log_filename}"

    try:
        result = subprocess.run(tee_command, shell=True)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print(f"\n\033[1;31m[-] Process terminated by operator. Log saved to {log_filename}\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
