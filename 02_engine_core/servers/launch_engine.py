#!/usr/bin/env python3
"""
===============================================================================
CATHEDRAL ENGINE - TURNKEY MASTER LAUNCHER
Usage:
  python3 launch_engine.py          # Start API server + launch Godot client
  python3 launch_engine.py --client # Launch Godot client only
  python3 launch_engine.py --server # Launch API server only
  python3 launch_engine.py --editor # Open project in Godot 4 Editor GUI
  python3 launch_engine.py --test   # Run full 5-subsystem test suite
===============================================================================
"""

from __future__ import annotations
import sys
import os
import time
import signal
import shutil
import urllib.request
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ANSI Formatting
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GREEN = "\033[92m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_CYAN = "\033[96m"
C_DIM = "\033[2m"

def find_godot_bin() -> str:
    candidates = [
        os.path.expanduser("~/.local/bin/godot"),
        shutil.which("godot"),
        "/Applications/Godot.app/Contents/MacOS/Godot",
        "/Applications/Godot_mono.app/Contents/MacOS/Godot"
    ]
    for c in candidates:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return ""

def print_banner():
    print(f"\n{C_BOLD}{C_CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║                     CATHEDRAL ENGINE - TURNKEY RUNTIME                       ║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║              Emotion = Physics = Magic = Biology = Architecture              ║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

def check_server_running() -> bool:
    try:
        req = urllib.request.Request("http://localhost:5050/api/rpg/state")
        with urllib.request.urlopen(req, timeout=0.8) as resp:
            return resp.status == 200
    except Exception:
        return False

def start_server_background() -> subprocess.Popen:
    print(f"  {C_CYAN}--> Starting Cathedral Backend API Server (port 5050)...{C_RESET}")
    cmd = [sys.executable, os.path.join(BASE_DIR, "server.py")]
    proc = subprocess.Popen(cmd, cwd=BASE_DIR)
    
    # Wait for server readiness
    for _ in range(15):
        time.sleep(0.2)
        if check_server_running():
            print(f"  {C_GREEN}✓ Backend API Server is online:{C_RESET} http://localhost:5050\n")
            return proc
            
    print(f"  {C_YELLOW}[!] Server started, proceeding with client launch...{C_RESET}\n")
    return proc

def launch_godot_client(godot_bin: str, editor_mode: bool = False):
    if not godot_bin:
        print(f"  {C_RED}[ERROR] Godot 4 executable not found. Please install Godot or place it in PATH.{C_RESET}")
        sys.exit(1)
        
    mode_str = "Godot 4 Editor" if editor_mode else "Interactive Client"
    print(f"  {C_CYAN}--> Launching {mode_str}...{C_RESET}")
    print(f"  {C_DIM}Binary:{C_RESET} {godot_bin}\n")
    
    args = [godot_bin]
    if editor_mode:
        args.append("-e")
        
    try:
        subprocess.run(args, cwd=BASE_DIR)
    except KeyboardInterrupt:
        pass

def main():
    args = set(sys.argv[1:])
    
    if "--test" in args:
        test_script = os.path.join(BASE_DIR, "run_tests.py")
        sys.exit(subprocess.run([sys.executable, test_script], cwd=BASE_DIR).returncode)
        
    print_banner()
    godot_bin = find_godot_bin()
        
    if "--server" in args:
        print(f"  {C_CYAN}--> Running Cathedral Backend Server in foreground...{C_RESET}")
        cmd = [sys.executable, os.path.join(BASE_DIR, "server.py")]
        try:
            subprocess.run(cmd, cwd=BASE_DIR)
        except KeyboardInterrupt:
            print(f"\n  {C_YELLOW}Server stopped.{C_RESET}")
        return

    if "--editor" in args:
        launch_godot_client(godot_bin, editor_mode=True)
        return

    if "--client" in args:
        launch_godot_client(godot_bin, editor_mode=False)
        return

    # Default turnkey mode: Server + Client
    server_proc = None
    if not check_server_running():
        server_proc = start_server_background()
    else:
        print(f"  {C_GREEN}✓ Existing Cathedral API Server detected on port 5050.{C_RESET}\n")
        
    try:
        launch_godot_client(godot_bin, editor_mode=False)
    finally:
        if server_proc:
            print(f"\n  {C_CYAN}--> Shutting down background API server...{C_RESET}")
            server_proc.terminate()
            try:
                server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_proc.kill()
            print(f"  {C_GREEN}✓ Server stopped cleanly.{C_RESET}\n")

if __name__ == "__main__":
    main()
