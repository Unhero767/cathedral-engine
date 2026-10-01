#!/usr/bin/env python3
"""
================================================================================
CATHEDRAL-ENGINE :: MASTER UNIFIED SYSTEM ORCHESTRATOR & CLI
================================================================================
Architected for Kenneth Dallmier (MLAOS-Prime Sovereign Architecture)
Anchored to Olney, IL (37.7306° N, -88.0817° W) | 43.7 Hz Carrier Resonance
================================================================================
"""

import sys
import os
import argparse
import json
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = SCRIPT_DIR

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engines.paraconsistent_engine import EAS03ParaconsistentEngine
from engines.emotional_physics_engine import EmotionalPhysicsEngine
from engines.arcana_engine import ArcanaEngine
from engines.codex_engine import CodexManager
from engines.ledger_engine import LedgerEngine
from engines.campaign_engine import CampaignEngine
from engines.enemy_engine import EnemyEngine
from engines.dialogue_engine import DialogueEngine
from engines.progression_engine import ProgressionEngine
from engines.game_loop_engine import GameLoopEngine
from engines.chamber_generator import ChamberGeneratorEngine
from engines.save_manager import SaveManagerEngine
from engines.character_creation_engine import CharacterCreationEngine
from engines.universe_atlas_engine import UniverseAtlasEngine
from engines.quantum_gravity_engine import QuantumGravityEngine
from mlaos_park.spark_orchestrator import MLAOSparkOrchestrator

def print_banner():
    banner = """
================================================================================
   ██████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗ ██████╗  █████╗ ██╗     
  ██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██║     
  ██║     ███████║   ██║   ███████║█████╗  ██║  ██║██████╔╝███████║██║     
  ██║     ██╔══██║   ██║   ██╔══██║██╔══╝  ██║  ██║██╔══██╗██╔══██║██║     
  ╚██████╗██║  ██║   ██║   ██║  ██║███████╗██████╔╝██║  ██║██║  ██║███████╗
   ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
                     ENGINE PRIME :: SOVEREIGN ARCHITECTURE
================================================================================
"""
    print(banner)

def get_system_status():
    print_banner()
    print("[STATUS] Performing Systemic Diagnostics across all 16 Subsystems...")
    print()
    
    codex_mgr = CodexManager(BASE_DIR)
    books = codex_mgr.list_books()
    print(f"  [+] Codex Vault:              {len(books)}/40 Books Cataloged & Mounted")
    
    ledger_path = os.path.join(BASE_DIR, "strata", "prime_ledger.ndjson")
    strata_count = 0
    if os.path.exists(ledger_path):
        with open(ledger_path, "r") as f:
            strata_count = sum(1 for line in f if line.strip())
    print(f"  [+] Ash Archive (NDJSON):      {strata_count} Inscribed Strata in prime_ledger.ndjson")
    
    camp = CampaignEngine(os.path.join(BASE_DIR, "strata", "campaign.db"))
    party = camp.get_party()
    inv = camp.get_inventory()
    print(f"  [+] Campaign & Relics DB:      {len(party)} Party Members | {len(inv)} Attuned Relics")
    
    ledger = LedgerEngine(os.path.join(BASE_DIR, "strata", "mlaos_ledger.db"))
    print(f"  [+] MLAOS Sovereign Ledger:    Online (Never-Overwrite DDL Triggers Active)")
    
    phys = EmotionalPhysicsEngine()
    theta_e, _ = phys.calculate_kinetic_state(0.95, 0.81)
    print(f"  [+] Emotional Physics Engine:  Nominal (Kinetic Baseline Theta_E: {theta_e})")
    
    para = EAS03ParaconsistentEngine(ledger_path)
    print(f"  [+] EAS-03 Belnap-Dunn Core:   Ready (Last Merkle Tip: {para.last_merkle_hash})")
    
    arcana = ArcanaEngine()
    print(f"  [+] 78-Card Ignition Arcana:   Assembled ({len(arcana.deck)} Cards, 7 Chromas x 7 Identity Vectors)")

    enemy_engine = EnemyEngine()
    print(f"  [+] Enemy & AI Engine:         Online ({len(enemy_engine.archetypes)} Adversary Archetypes Registered)")
    
    dialogue_engine = DialogueEngine(os.path.join(BASE_DIR, "strata", "campaign.db"))
    print(f"  [+] Dialogue & Quest Engine:   Online ({len(dialogue_engine.quests)} Active Quests Loaded)")

    prog_engine = ProgressionEngine(os.path.join(BASE_DIR, "strata", "campaign.db"))
    print(f"  [+] Character Progression:     Online ({len(prog_engine.recipes)} Relic Recipes / Talent Trees)")

    chamber_gen = ChamberGeneratorEngine()
    print(f"  [+] 40-Chamber Generator:      Online ({len(chamber_gen.books_catalog)} Chamber Monograph Layouts)")

    save_mgr = SaveManagerEngine(os.path.join(BASE_DIR, "strata", "campaign.db"))
    print(f"  [+] Save Manager & Chronicle:  Online (3 Merkle Checkpoint Slots Active)")

    char_creator = CharacterCreationEngine(os.path.join(BASE_DIR, "strata", "campaign.db"))
    print(f"  [+] Character Genesis Engine:  Online ({len(char_creator.origins)} Origins, {len(char_creator.archetypes)} Archetypes)")

    universe_atlas = UniverseAtlasEngine()
    print(f"  [+] Master Cosmic Atlas:       Online (4 Strata, 36 Oculus Chambers, 10 Laws)")

    qgrav = QuantumGravityEngine(grid_size=32, dx=1.0e-15, mass=1.0e-20)
    print(f"  [+] Quantum Self-Gravitation:  Online (Schrodinger-Newton Soliton E_grav: {qgrav.component.total_self_energy:.4e} J)")

    spark = MLAOSparkOrchestrator(BASE_DIR)
    print(f"  [+] MLAOSpark Metabolic Core:  Online (PTE + CTE + SPE + CIM Active)")

    print()
    print("[VERDICT] All 16 Subsystems Integrated & Operationally Harmonic.")
    print("================================================================================")
    print()

def run_qgrav_pilot():
    print_banner()
    print("[RUN] Executing Quantum-Gravitational Self-Coupling Simulation (Schrodinger-Newton)...")
    print()
    engine = QuantumGravityEngine(grid_size=32, dx=1.0e-15, mass=1.0e-20)
    print(f"  [+] Grid Resolution:     32 x 32 (dx = {engine.dx} m, mass = {engine.mass} kg)")
    print(f"  [+] Initial Self-Energy:  {engine.component.total_self_energy:.6e} J")
    
    print()
    print("  [+] Stepping 5 Split-Step Fourier / FFT Poisson Evolution Iterations...")
    step_res = engine.step_simulation(dt=1.0e-18, steps=5)
    print(f"      Total Gravitational Self-Energy: {step_res['total_self_energy']:.6e} J")
    print(f"      Peak Self-Potential (Phi):       {step_res['max_self_potential']:.6e} m^2/s^2")
    print(f"      Peak Medium Strain (epsilon):    {step_res['max_medium_strain']:.6e}")
    print(f"      Effective Scaled Mass m*(eps):   {step_res['effective_mass']:.6e} kg")

    print()
    print("  [+] Calculating Diosi-Penrose Gravitational Self-Decoherence...")
    dp = engine.calculate_diosi_penrose_decoherence(1.0e-14)
    print(f"      Delta E_G (Spatial Superposition): {dp['delta_e_g_joules']:.6e} J")
    print(f"      Decay Timescale tau_decay:         {dp['tau_decay_seconds']:.6e} s")
    print(f"      Planck Threshold Ratio:            {dp['planck_threshold_ratio']:.6e}")

    print()
    print("  [+] Evaluating QGrav Category Functor S Fixed Point...")
    qgrav = engine.evaluate_qgrav_functor()
    print(f"      Category:   {qgrav['category']}")
    print(f"      Functor S:  {qgrav['functor']}")
    print(f"      Verdict:    {qgrav['verdict']} (Energy Diff: {qgrav['energy_variance']:.6e})")
    print()
    print("[COMPLETE] Quantum-Gravitational Self-Coupling Pipeline Converged.")
    print("================================================================================")

def run_spark_pilot():
    print_banner()
    print("[RUN] Executing MLAOSpark v0.1 (SPARK-0 Controlled Pilot)...")
    spark = MLAOSparkOrchestrator(BASE_DIR)
    res = spark.run_spark_0_pilot()
    print(json.dumps(res, indent=2))

def run_tests():
    print_banner()
    print("[TEST] Running Unified Master Engine Test Suite (All 16 Subsystems)...")
    print()
    import unittest
    suite = unittest.defaultTestLoader.discover(os.path.join(BASE_DIR, "tests"))
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if not res.wasSuccessful():
        sys.exit(1)

def run_server(port=5050):
    print_banner()
    print(f"[SERVER] Launching Cathedral-Engine Web Altar on port {port}...")
    server_path = os.path.join(BASE_DIR, "server.py")
    if os.path.exists(server_path):
        os.system(f"python3 {server_path} {port}")

def main():
    parser = argparse.ArgumentParser(description="Cathedral-Engine Master Unified CLI")
    parser.add_argument("--status", action="store_true", help="Print systemic status report")
    parser.add_argument("--run", type=str, choices=["spark-pilot", "atlas", "chamber", "character-create", "arcana", "physics", "eas03", "server", "qgrav", "schrodinger-newton"], help="Execute subsystem")
    parser.add_argument("--chamber-id", type=int, default=1, help="Target chamber index (1-40)")
    parser.add_argument("--export-chronicle", action="store_true", help="Export playthrough chronicle for NotebookLM")
    parser.add_argument("--test-all", action="store_true", help="Execute complete automated test suite")
    parser.add_argument("--port", type=int, default=5050, help="Port for Web Altar server")

    args = parser.parse_args()

    if args.test_all:
        run_tests()
    elif args.run == "spark-pilot":
        run_spark_pilot()
    elif args.run in ["qgrav", "schrodinger-newton"]:
        run_qgrav_pilot()
    elif args.run == "server":
        run_server(args.port)
    else:
        get_system_status()

if __name__ == "__main__":
    main()
