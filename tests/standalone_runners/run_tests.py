#!/usr/bin/env python3
"""
===============================================================================
CATHEDRAL ENGINE - UNIFIED TEST SUITE & CI HARNESS
Validates:
  1. Cathedral Master Engine & Belnap-Dunn Lattice (cathedral_engine.py)
  2. EAS-03 Paraconsistent Frame Collision & Merkle DAG (02_engine_core)
  3. Local HTTP Server & API Endpoints (server.py)
  4. Godot 4 Headless Project Compilation & Resource Bindings
  5. Godot 4 Scene Execution (CathedralAvatarDemo & Spatial Triad)
===============================================================================
"""

from __future__ import annotations
import sys
import os
import time
import json
import shutil
import urllib.request
import subprocess
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ANSI Colors
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

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.duration_s = 0.0
        self.message = ""

def run_test_master_engine() -> TestResult:
    res = TestResult("Cathedral Master Engine & Paraconsistent Lattice")
    t0 = time.time()
    try:
        script_path = os.path.join(BASE_DIR, "cathedral_engine.py")
        cmd = [sys.executable, script_path, "--test"]
        proc = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, timeout=10)
        if proc.returncode == 0 and "PASS" in proc.stdout:
            res.passed = True
            res.message = "Paraconsistent lattice meet/join & Ash Archive Merkle DAG passed."
        else:
            res.passed = False
            res.message = proc.stderr.strip() or proc.stdout.strip() or f"Exit code {proc.returncode}"
    except Exception as exc:
        res.passed = False
        res.message = str(exc)
    finally:
        res.duration_s = time.time() - t0
    return res

def run_test_eas03_engine() -> TestResult:
    res = TestResult("EAS-03 Paraconsistent Frame Collision Engine")
    t0 = time.time()
    try:
        core_dir = os.path.join(BASE_DIR, "02_engine_core", "logic_engines")
        sys.path.insert(0, core_dir)
        from paraconsistent_engine import EAS03ParaconsistentEngine, BelnapDunnTruthState
        
        tmp_ledger = os.path.join(BASE_DIR, "quarantine_archive", "test_ledger.ndjson")
        engine = EAS03ParaconsistentEngine(ledger_path=tmp_ledger)
        
        # Dialetheic superposition frame test
        frame1 = engine.process_frame_tick(1, c_pos=0.8, c_neg=0.8)
        assert frame1["state"] == BelnapDunnTruthState.BOTH
        assert frame1["merkle_tip"] != ""
        
        # Clean temporary test ledger
        if os.path.exists(tmp_ledger):
            os.remove(tmp_ledger)
            
        res.passed = True
        res.message = f"Processed 60Hz tick; generated Merkle tip: {frame1['merkle_tip'][:18]}..."
    except Exception as exc:
        res.passed = False
        res.message = str(exc)
    finally:
        res.duration_s = time.time() - t0
    return res

def run_test_http_server() -> TestResult:
    res = TestResult("Cathedral Local HTTP/REST API Server")
    t0 = time.time()
    server_proc = None
    try:
        # Launch server.py in subprocess
        cmd = [sys.executable, os.path.join(BASE_DIR, "server.py")]
        server_proc = subprocess.Popen(cmd, cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait up to 3 seconds for server to respond
        time.sleep(0.8)
        req = urllib.request.Request("http://localhost:5050/api/rpg/state")
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            assert "game_state" in data
            assert data["game_state"] == "RUNNING"
            
        # Test move endpoint
        req_move = urllib.request.Request("http://localhost:5050/api/rpg/move?x=10&y=12&chamber=3")
        with urllib.request.urlopen(req_move, timeout=2.0) as resp:
            move_data = json.loads(resp.read().decode('utf-8'))
            assert move_data.get("status") == "MOVED"
            assert move_data.get("x") == 10
            
        res.passed = True
        res.message = f"HTTP 200 on /api/rpg/state & /api/rpg/move (State: {data['game_state']})"
    except Exception as exc:
        res.passed = False
        res.message = str(exc)
    finally:
        if server_proc:
            server_proc.terminate()
            server_proc.wait()
        res.duration_s = time.time() - t0
    return res

def run_test_godot_headless(godot_bin: str) -> TestResult:
    res = TestResult("Godot 4 Project Compilation & Script Validation")
    t0 = time.time()
    if not godot_bin:
        res.passed = False
        res.message = "Godot binary not detected in environment."
        res.duration_s = 0.0
        return res
        
    try:
        cmd = [godot_bin, "--headless", "--quit"]
        proc = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, timeout=10)
        
        # Check stderr for GDScript SCRIPT ERROR or Parse Error
        output = proc.stdout + proc.stderr
        has_error = proc.returncode != 0 or "SCRIPT ERROR" in output or "Parse Error" in output
        
        if not has_error:
            res.passed = True
            res.message = "Engine loaded and validated project with 0 parse errors."
        else:
            res.passed = False
            # Extract first error line
            err_lines = [l for l in output.splitlines() if "ERROR" in l or "Error" in l]
            res.message = err_lines[0] if err_lines else f"Exit code {proc.returncode}"
    except Exception as exc:
        res.passed = False
        res.message = str(exc)
    finally:
        res.duration_s = time.time() - t0
    return res

def run_test_godot_scenes(godot_bin: str) -> TestResult:
    res = TestResult("Godot 4 Scene Simulation (CathedralAvatarDemo & Triad)")
    t0 = time.time()
    if not godot_bin:
        res.passed = False
        res.message = "Godot binary not detected in environment."
        res.duration_s = 0.0
        return res
        
    try:
        # Run main scene for 30 frames
        cmd_main = [godot_bin, "--headless", "--quit-after", "30"]
        proc_main = subprocess.run(cmd_main, cwd=BASE_DIR, capture_output=True, text=True, timeout=15)
        
        # Run secondary triad scene for 30 frames
        triad_scene = "03_godot_client/scenes/spatial_triad_demo_scene.tscn"
        cmd_triad = [godot_bin, "--headless", triad_scene, "--quit-after", "30"]
        proc_triad = subprocess.run(cmd_triad, cwd=BASE_DIR, capture_output=True, text=True, timeout=15)
        
        main_ok = proc_main.returncode == 0 and "SCRIPT ERROR" not in proc_main.stdout
        triad_ok = proc_triad.returncode == 0 and "SCRIPT ERROR" not in proc_triad.stdout
        
        if main_ok and triad_ok:
            res.passed = True
            res.message = "Main Scene & Spatial Triad executed 30 frames cleanly."
        else:
            res.passed = False
            res.message = f"Simulation failed (Main Code: {proc_main.returncode}, Triad Code: {proc_triad.returncode})"
    except Exception as exc:
        res.passed = False
        res.message = str(exc)
    finally:
        res.duration_s = time.time() - t0
    return res

def main():
    print(f"\n{C_BOLD}{C_CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║                 CATHEDRAL ENGINE - UNIFIED TEST SUITE                        ║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")
    
    godot_bin = find_godot_bin()
    if godot_bin:
        print(f"  {C_DIM}Detected Godot 4 Binary:{C_RESET} {C_GREEN}{godot_bin}{C_RESET}")
    else:
        print(f"  {C_DIM}Detected Godot 4 Binary:{C_RESET} {C_YELLOW}None (Godot tests will be skipped){C_RESET}")
    print(f"  {C_DIM}Base Directory:{C_RESET}          {BASE_DIR}\n")
    
    tests = [
        run_test_master_engine,
        run_test_eas03_engine,
        run_test_http_server,
        lambda: run_test_godot_headless(godot_bin),
        lambda: run_test_godot_scenes(godot_bin)
    ]
    
    results: list[TestResult] = []
    
    for t_fn in tests:
        res = t_fn()
        results.append(res)
        status_badge = f"{C_BOLD}{C_GREEN}PASS{C_RESET}" if res.passed else f"{C_BOLD}{C_RED}FAIL{C_RESET}"
        print(f"  [{status_badge}] {C_BOLD}{res.name}{C_RESET} ({res.duration_s:.2f}s)")
        print(f"         {C_DIM}{res.message}{C_RESET}")
    
    all_passed = all(r.passed for r in results)
    total_time = sum(r.duration_s for r in results)
    
    print(f"\n{C_CYAN}──────────────────────────────────────────────────────────────────────────────{C_RESET}")
    if all_passed:
        print(f"  {C_BOLD}{C_GREEN}✓ ALL {len(results)} SUB-SYSTEM TESTS PASSED SUCCESSFULLY{C_RESET} ({total_time:.2f}s total)")
        print(f"{C_CYAN}──────────────────────────────────────────────────────────────────────────────{C_RESET}\n")
        sys.exit(0)
    else:
        failed_count = sum(1 for r in results if not r.passed)
        print(f"  {C_BOLD}{C_RED}✗ {failed_count} OF {len(results)} TESTS FAILED{C_RESET} ({total_time:.2f}s total)")
        print(f"{C_CYAN}──────────────────────────────────────────────────────────────────────────────{C_RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
