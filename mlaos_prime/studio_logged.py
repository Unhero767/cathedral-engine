#!/usr/bin/env python3
# ====================================================================
# MLAOS-Prime :: Unified Studio Execution & Logging Engine
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import sys
import subprocess
import os
import time

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
    print("\033[1;36m│   CATHEDRAL STUDIO LOGGED EXECUTION    │\033[0m")
    print("\033[1;36m└────────────────────────────────────────┘\033[0m")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TASKS:
        render_banner()
        print("Usage: studio_logged [command]\n\nAvailable Commands:")
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
    os.makedirs("logs", exist_ok=True)
    log_file_path = f"logs/{action}_{int(time.time())}.log"
    
    print(f"\033[1;33m==> Executing [Logged to {log_file_path}]: {command_str}\033[0m")
    
    # Wrap with tee-like shell redirection to preserve live terminal streaming while logging output
    logged_command_str = f"{command_str} 2>&1 | tee {log_file_path}"
    
    try:
        result = subprocess.run(logged_command_str, shell=True)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print(f"\n\033[1;31m[-] Process terminated by operator. Logs saved to {log_file_path}\033[0m")
        sys.exit(0)

if __name__ == "__main__":
    main()
