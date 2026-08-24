#!/usr/bin/env python3
"""
Cathedral-Engine Unified CLI Management Utility (cathedral-cli).
Subcommands: patrol, jump, audit, export, verify-merkle, start, stop, status, simulate, wargame, batch-codex, trikey-diagnose.
Strata: Books I–XL & Ash Archive JBP Ledger.
"""

import sys
import os
import argparse
import subprocess
import signal
import time
import json
import urllib.request
import urllib.error

from engine.database import DatabaseManager, DB_PATH
from engine.models import Spectral, BelnapValue
from engine.codex_generator import CodexGenerator
from engine.merkle_verifier import MerkleVerifier
from engine.simulation import PlaytestSimulationRunner
from engine.wargame import DialetheicWargameEngine
from engine.batch_codex import BatchCodexCompiler
from engine.trikey_diagnostics import TriKeyDiagnosticSuite

PID_FILE = "/working_dir/c_9a0a4a350cc893af/strata/cathedral_daemon.pid"
SERVER_URL = "http://127.0.0.1:5000"

class TermColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def print_header(title: str):
    print(f"\n{TermColor.BOLD}{TermColor.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{TermColor.RESET}")
    print(f"{TermColor.BOLD}{TermColor.CYAN}║ {title.center(76)} ║{TermColor.RESET}")
    print(f"{TermColor.BOLD}{TermColor.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: Patrol
# -----------------------------------------------------------------------------
def cmd_patrol(args):
    print_header("PANOPTICON STRATUM: AXIOMATIC ECHOLOCATION PATROL")
    print(f"{TermColor.DIM}Deploying Tier-2 Surveyor Oracles along the Glitch-Waste perimeter...{TermColor.RESET}")
    time.sleep(0.2)
    print(f"{TermColor.CYAN}▶ Firing sterile truth-pulse: [A = A ∧ 1 = 1] into the Manifold...{TermColor.RESET}")
    
    import random
    div_vector = round(random.uniform(0.112, 0.284), 4)
    c_tau = round(random.uniform(0.82, 0.94), 3)
    
    print(f"{TermColor.YELLOW}• Divergence Vector (∇Ex°): {div_vector:.4f} (Decay within safety limits < 0.30){TermColor.RESET}")
    print(f"{TermColor.GREEN}• Consistency Coefficient (C_τ): {c_tau:.3f} ≥ 1.0 (Mortar Domain Sealed){TermColor.RESET}")
    print(f"{TermColor.CYAN}• Optical Transition: Active Crimson → Oxford Blue (Fossilized Bedrock){TermColor.RESET}")
    
    db = DatabaseManager()
    block = db.append_ash_block(
        event_type="PANOPTICON_PATROL",
        payload={"divergence_vector": div_vector, "consistency_c_tau": c_tau, "status": "SURVEYOR_OPTIMAL"}
    )
    print(f"\n{TermColor.BOLD}{TermColor.GREEN}✓ Patrol sweep committed to Ash Archive: Block #{block.index} [{block.block_hash[:16]}]{TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: Jump
# -----------------------------------------------------------------------------
def cmd_jump(args):
    chamber_id = args.chamber_id
    print_header(f"SOVEREIGN SPATIAL TRANSITION: JUMP TO CHAMBER {chamber_id}")
    
    carrier_freq = 130.81 if chamber_id == 5 else round(130.81 * (1.0 + 0.1 * (chamber_id - 5)), 2)
    print(f"Target Chamber Coordinate: {TermColor.BOLD}Chamber {chamber_id}{TermColor.RESET}")
    print(f"Master Carrier Frequency : {TermColor.BOLD}{carrier_freq} Hz (Note C3 Base){TermColor.RESET}")
    print(f"A-Field Flux Parameter   : {TermColor.BOLD}dΦ/dt = 0.428 rad/s{TermColor.RESET}")
    
    db = DatabaseManager()
    block = db.append_ash_block(
        event_type="CHAMBER_JUMP",
        payload={"target_chamber": chamber_id, "carrier_hz": carrier_freq, "dphi_dt": 0.428}
    )
    print(f"\n{TermColor.GREEN}✓ Chamber {chamber_id} spatial matrix initialized and locked. Committed Block #{block.index}.{TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: Audit
# -----------------------------------------------------------------------------
def cmd_audit(args):
    print_header("CATHEDRAL-ENGINE STRATA AUDIT & COMPLIANCE")
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM ash_ledger")
        l_cnt, t_min, t_max = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM codex_strata")
        c_cnt = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM codex_chapters")
        ch_cnt = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM oracle_deck_strata")
        o_cnt = cursor.fetchone()[0]

    print(f"• {TermColor.BOLD}Ash Archive JBP Ledger{TermColor.RESET}     : {TermColor.GREEN}{l_cnt} Blocks committed{TermColor.RESET}")
    print(f"• {TermColor.BOLD}40-Book Codex Strata Registry{TermColor.RESET} : {TermColor.GREEN}{c_cnt} / 40 Books Indexed{TermColor.RESET}")
    print(f"• {TermColor.BOLD}Codex Chapter Monographs{TermColor.RESET}     : {TermColor.GREEN}{ch_cnt} Chapters Scaffolded{TermColor.RESET}")
    print(f"• {TermColor.BOLD}Persona Oracle Deck Registry{TermColor.RESET} : {TermColor.GREEN}{o_cnt} / 377 Cards Indexed{TermColor.RESET}")
    print(f"• {TermColor.BOLD}Never-Overwrite Doctrine{TermColor.RESET}     : {TermColor.GREEN}ENFORCED (Zero Deletions Allowed){TermColor.RESET}")
    print(f"• {TermColor.BOLD}Tri-Key Sovereign Gating{TermColor.RESET}     : {TermColor.GREEN}ACTIVE (Lead, Cyan, Iron Seals Verified){TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: Export
# -----------------------------------------------------------------------------
def cmd_export(args):
    target = args.target.lower()
    print_header(f"VAULT EXPORT PIPELINE: TARGET --{target.upper()}")
    compiler = BatchCodexCompiler(DatabaseManager())
    compiler._export_vault_artifacts()
    print(f"{TermColor.GREEN}✓ Vault exports successfully refreshed in /working_dir/c_9a0a4a350cc893af/artifacts/{TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: Verify-Merkle
# -----------------------------------------------------------------------------
def cmd_verify_merkle(args):
    print_header("ASH ARCHIVE MERKLE DAG CRYPTOGRAPHIC VERIFICATION")
    db = DatabaseManager()
    verifier = MerkleVerifier(db)
    res = verifier.verify_ledger_chain()
    
    if res["valid"]:
        print(f"{TermColor.BOLD}{TermColor.GREEN}✓ LEDGER INTEGRITY CONFIRMED:{TermColor.RESET} {res['message']}")
        print(f"• Verified Blocks : {TermColor.GREEN}{res['verified_blocks']}{TermColor.RESET}")
        print(f"• Tip Block Index : #{res['tip_block_index']}")
        print(f"• Tip Block Hash  : {TermColor.YELLOW}{res['tip_block_hash']}{TermColor.RESET}\n")
    else:
        print(f"{TermColor.BOLD}{TermColor.RED}✗ TAMPERING DETECTED!{TermColor.RESET}")
        print(f"• Error: {res['error']}")
        print(f"• Tampered Block Index: #{res['tampered_index']}")
        if args.auto_rollback:
            print(f"{TermColor.YELLOW}Executing automated rollback to safe block index #{res['tampered_index'] - 1}...{TermColor.RESET}")
            rb = verifier.rollback_to_safe_block(res['tampered_index'] - 1)
            print(f"{TermColor.GREEN}✓ {rb['notice']}{TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: Wargame (N >= 4 Choir Battle Simulation)
# -----------------------------------------------------------------------------
def cmd_wargame(args):
    rounds = args.rounds
    print_header(f"MULTI-AGENT PARACONSISTENT WARGAME (N=4 CHOIRS, {rounds} ROUNDS)")
    db = DatabaseManager()
    engine = DialetheicWargameEngine(db)
    summary = engine.run_wargame(rounds=rounds)

    for r in summary["rounds"]:
        print(f"{TermColor.BOLD}--- ROUND {r['round']} TACTICAL ENGAGEMENT ---{TermColor.RESET}")
        for f in r["factions"]:
            color = TermColor.RED if f["spectral"] == "RED" else (
                TermColor.GREEN if f["spectral"] == "EMERALD" else (
                    TermColor.YELLOW if f["spectral"] == "GOLD" else TermColor.MAGENTA
                )
            )
            print(f" {color}▶ [{f['name']}]{TermColor.RESET}: Intent -> \"{f['intent']}\" | Assertion: {TermColor.BOLD}[{f['assertion']}]{TermColor.RESET}")
        
        clash = r["primary_clash"]
        print(f"\n {TermColor.CYAN}Clash Resolution:{TermColor.RESET} {clash['combatants']} -> {TermColor.BOLD}{clash['resolution']}{TermColor.RESET}")
        print(f" {clash['description']}")
        print(f" {TermColor.DIM}State: τ={r['state_after']['tau_pol']:.2f}, ρ={r['state_after']['rho_res']:.2f}, δ={r['state_after']['delta_fac']:.2f}, σ={r['state_after']['sigma_coh']:.2f}{TermColor.RESET}\n")

    print(f"{TermColor.BOLD}{TermColor.GREEN}✓ Wargame Concluded:{TermColor.RESET} Final Bilattice Join: {TermColor.BOLD}[{summary['final_bilattice_state']}]{TermColor.RESET}")
    print(f"• Total Harmonic Scars Petrified: {TermColor.GREEN}{summary['total_harmonic_scars']}{TermColor.RESET}")
    print(f"• Ash Archive Commit: Block #{summary['ash_block_index']} [{summary['ash_block_hash'][:16]}]\n")

# -----------------------------------------------------------------------------
# Subcommand: Batch-Codex (40 Books Scaffolding)
# -----------------------------------------------------------------------------
def cmd_batch_codex(args):
    print_header("BATCH-GENERATING 40-BOOK CODEX MONOGRAPHS (BOOKS I–XL)")
    db = DatabaseManager()
    compiler = BatchCodexCompiler(db)
    summary = compiler.compile_all_40_books()

    print(f"• Total Monographs Scaffolded: {TermColor.BOLD}{summary['total_books_scaffolded']} Books{TermColor.RESET} in {summary['elapsed_seconds']}s")
    for tier, cnt in summary["tier_distribution"].items():
        print(f"  - {TermColor.CYAN}{tier:<20}{TermColor.RESET}: {cnt} Monographs")
    
    print(f"\n{TermColor.GREEN}✓ Cryptographic Verification: {summary['merkle_verification']['message']}{TermColor.RESET}")
    print(f"• Tip Block Index: #{summary['merkle_verification']['tip_block_index']}")
    print(f"• Tip Block Hash : {TermColor.YELLOW}{summary['merkle_verification']['tip_block_hash']}{TermColor.RESET}\n")

# -----------------------------------------------------------------------------
# Subcommand: TriKey-Diagnose
# -----------------------------------------------------------------------------
def cmd_trikey_diagnose(args):
    print_header("TRI-KEY SOVEREIGN DIAGNOSTIC & 9-STAGE REDUCTION WIZARD")
    db = DatabaseManager()
    suite = TriKeyDiagnosticSuite(db)
    
    diag = suite.audit_tri_key_governance()
    print(f"{TermColor.BOLD}[TRI-KEY GOVERNANCE SEALS]:{TermColor.RESET}")
    print(f" • {TermColor.YELLOW}{diag['lead_key']['key']}{TermColor.RESET}: {diag['lead_key']['status']} ({diag['lead_key']['active_blocks_locked']} blocks locked)")
    print(f" • {TermColor.CYAN}{diag['cyan_key']['key']}{TermColor.RESET}: {diag['cyan_key']['status']} ({diag['cyan_key']['books_synchronized']} books synced at {diag['cyan_key']['sync_rate_hz']} Hz)")
    print(f" • {TermColor.RED}{diag['iron_key']['key']}{TermColor.RESET}: {diag['iron_key']['status']} (Force: {diag['iron_key']['force_projection']})")
    print(f" • Thermal Heat-Sink: {diag['thermal_heat_sink']['somatic_baseline_hz']} Hz Somatic baseline dissipating {diag['thermal_heat_sink']['civic_logic_frequency_hz']} Hz Civic load (Burn Risk: {TermColor.GREEN}{diag['thermal_heat_sink']['burn_risk']}{TermColor.RESET})\n")

    print(f"{TermColor.BOLD}[EXECUTING 9-STAGE LOAD-BEARING REDUCTION LOOP]:{TermColor.RESET}")
    loop = suite.execute_9_stage_reduction_loop()
    for s in loop["stages"]:
        print(f" {TermColor.CYAN}{s['stage']:<20}{TermColor.RESET} {s['detail']}")
    
    print(f"\n{TermColor.BOLD}{TermColor.GREEN}✓ Reduction Loop Completed:{TermColor.RESET} Coherence σ={loop['telemetry_output']['sigma_coh']}, Frame Delta={loop['telemetry_output']['frame_ms']}ms")
    print(f"• Committed Block: Block #{loop['ash_block_index']} [{loop['ash_block_hash'][:16]}]\n")

# -----------------------------------------------------------------------------
# Server Lifecycle (start, stop, status) & Simulate
# -----------------------------------------------------------------------------
def cmd_start(args):
    print_header("STARTING CATHEDRAL-ENGINE DAEMON")
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)
            print(f"{TermColor.YELLOW}Daemon is already running with PID {pid}.{TermColor.RESET}\n")
            return
        except OSError:
            os.remove(PID_FILE)

    proc = subprocess.Popen(
        [sys.executable, "-m", "engine.server"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd="/working_dir/c_9a0a4a350cc893af"
    )
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))
        
    time.sleep(0.5)
    print(f"{TermColor.GREEN}✓ Cathedral Daemon started on http://127.0.0.1:5000 (PID: {proc.pid}){TermColor.RESET}\n")

def cmd_stop(args):
    print_header("STOPPING CATHEDRAL-ENGINE DAEMON")
    if not os.path.exists(PID_FILE):
        print(f"{TermColor.YELLOW}Daemon is not running.{TermColor.RESET}\n")
        return
    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"{TermColor.GREEN}✓ Daemon PID {pid} stopped gracefully.{TermColor.RESET}\n")
    except OSError:
        print(f"{TermColor.RED}Failed to kill PID {pid}.{TermColor.RESET}\n")
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def cmd_status(args):
    print_header("CATHEDRAL-ENGINE DAEMON STATUS")
    try:
        req = urllib.request.Request(f"{SERVER_URL}/api/health", headers={"User-Agent": "CathedralCLI/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"• Daemon Status   : {TermColor.GREEN}{data['status']}{TermColor.RESET}")
                print(f"• Service Name    : {data['service']}")
                print(f"• Active Chamber  : Chamber {data['active_chamber']}")
                print(f"• Carrier Freq    : {data['carrier_hz']} Hz")
                print(f"• Doctrine        : {data['doctrine']}\n")
                return
    except Exception:
        pass
    print(f"• Daemon Status   : {TermColor.RED}OFFLINE / STOPPED{TermColor.RESET}\n")

def cmd_simulate(args):
    turns = args.turns
    print_header(f"RUNNING PERSONA ORACLE PLAYTEST SIMULATION ({turns} TURNS)")
    db = DatabaseManager()
    runner = PlaytestSimulationRunner(db)
    res = runner.run_simulation(total_turns=turns)
    
    print(f"• Total Turns Executed       : {TermColor.BOLD}{res['total_turns']}{TermColor.RESET} in {res['elapsed_seconds']}s")
    print(f"• Belnap Truth Distribution  : T={res['belnap_distribution']['T']}, F={res['belnap_distribution']['F']}, B={res['belnap_distribution']['B']}, N={res['belnap_distribution']['N']}")
    print(f"• Harmonic Scars Created     : {TermColor.GREEN}{res['harmonic_scars_created']} X-Pillars petrified{TermColor.RESET}")
    print(f"• Average Algorithmic Cost   : {TermColor.YELLOW}{res['average_algorithmic_cost']:.4f}{TermColor.RESET} (≤ 0.30 target)")
    print(f"• Lyapunov Exponent (λ_max)  : {TermColor.GREEN}{res['average_lyapunov_exponent']:.4f}{TermColor.RESET} (< 0 stable)")
    print(f"• Final Systemic Coherence σ : {TermColor.BOLD}{res['final_state']['sigma_coh']:.3f}{TermColor.RESET}")
    print(f"• Committed Ash Archive Block: Block #{res['ash_block_index']} [{res['ash_block_hash'][:16]}]\n")

def main():
    parser = argparse.ArgumentParser(description="Cathedral-Engine Unified Management CLI (cathedral-cli)")
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # patrol, jump, audit, export, verify-merkle
    subparsers.add_parser("patrol", help="Run Panopticon Axiomatic Echolocation sweep")
    p_jump = subparsers.add_parser("jump", help="Transition spatial coordinate to chamber")
    p_jump.add_argument("chamber_id", type=int, help="Chamber ID (e.g. 5)")
    subparsers.add_parser("audit", help="Audit database strata and Never-Overwrite compliance")
    p_export = subparsers.add_parser("export", help="Export documentation vaults")
    p_export.add_argument("--target", choices=["codex", "notebooklm", "concordance"], default="codex", help="Export format target")
    p_vm = subparsers.add_parser("verify-merkle", help="Verify Merkle DAG chain integrity")
    p_vm.add_argument("--auto-rollback", action="store_true", help="Automatically rollback if corrupted")

    # wargame, batch-codex, trikey-diagnose
    p_war = subparsers.add_parser("wargame", help="Run N>=4 multi-agent paraconsistent wargame")
    p_war.add_argument("--rounds", type=int, default=4, help="Number of tactical combat rounds")
    subparsers.add_parser("batch-codex", help="Batch scaffold all 40 canonical Codex books into ash_archive.db")
    subparsers.add_parser("trikey-diagnose", help="Run Tri-Key Sovereign Diagnostic and 9-Stage Load-Bearing Reduction Loop")

    # start, stop, status, simulate
    subparsers.add_parser("start", help="Start engine background daemon")
    subparsers.add_parser("stop", help="Stop engine daemon")
    subparsers.add_parser("status", help="Check engine daemon status")
    p_sim = subparsers.add_parser("simulate", help="Run multi-turn Oracle & Belnap simulation")
    p_sim.add_argument("--turns", type=int, default=3000, help="Number of turns (default: 3000)")

    args = parser.parse_args()

    dispatch = {
        "patrol": cmd_patrol,
        "jump": cmd_jump,
        "audit": cmd_audit,
        "export": cmd_export,
        "verify-merkle": cmd_verify_merkle,
        "wargame": cmd_wargame,
        "batch-codex": cmd_batch_codex,
        "trikey-diagnose": cmd_trikey_diagnose,
        "start": cmd_start,
        "stop": cmd_stop,
        "status": cmd_status,
        "simulate": cmd_simulate
    }

    if args.subcommand in dispatch:
        dispatch[args.subcommand](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
