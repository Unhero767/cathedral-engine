"""
Path D & Branch J: Terminal Visualization Layer for Dialetheic Core & Ash Archive.
Renders ASCII/ANSI graph visualization of Harmonic Scars, paradox loads,
spectral tension metrics, and Ritual Telemetry Omens.
Supports --watch or --refresh N for live polling.
"""

import os
import sys
import time
import argparse
from typing import List, Dict, Any

# Bootstrapping sys.path for direct script execution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    from src.cathedral_engine import CathedralEngineSimulation, SpectrumConstant
    from src.vector_mapper import AshArchiveMapper
    from src.archive_store import ArchiveStore
    from src.ritual import RitualEngine
except ModuleNotFoundError:
    from cathedral_engine import CathedralEngineSimulation, SpectrumConstant
    from vector_mapper import AshArchiveMapper
    from archive_store import ArchiveStore
    from ritual import RitualEngine

ANSI_SPECTRAL_MAP = {
    SpectrumConstant.GOLD: "\033[93m",
    SpectrumConstant.TEAL: "\033[96m",
    SpectrumConstant.BLUE: "\033[94m",
    SpectrumConstant.RED: "\033[91m",
    SpectrumConstant.VIOLET: "\033[95m",
    SpectrumConstant.EMERALD: "\033[92m",
    SpectrumConstant.BRONZE_OBSIDIAN: "\033[90m",
}
RESET = "\033[0m"
BOLD = "\033[1m"


class CLIGraphDashboard:
    def __init__(self, mapper: AshArchiveMapper, simulation: CathedralEngineSimulation):
        self.mapper = mapper
        self.simulation = simulation

    def render_header(self):
        print(f"{BOLD}{'='*72}{RESET}")
        print(f"{BOLD} CATHEDRAL-ENGINE :: ASH ARCHIVE TENSION GRAPH DASHBOARD (PATH D + J){RESET}")
        print(f"{BOLD}{'='*72}{RESET}")
        print(f" A-Field Temp: {self.simulation.a_field_temp:.1f}K | Active Scars: {len(self.simulation.buffer.harmonic_scars)} | Flux: {self.simulation.hysteresis.current_flux:.2f}")
        print(f"{'-'*72}")

    def render_scar_nodes(self):
        print(f"{BOLD}[HARMONIC SCAR NODES & PARADOX TENSION MATRIX]{RESET}\n")
        scars = self.simulation.buffer.harmonic_scars
        if not scars:
            print("  (No active Harmonic Scars recorded in Dialetheic Buffer)")
            return

        for scar in scars:
            color = ANSI_SPECTRAL_MAP.get(scar.spectrum, RESET)
            load_bar_len = int(scar.contradiction_degree * 3)
            load_bar = "█" * load_bar_len + "░" * (30 - load_bar_len)
            
            print(f"  Node ID : {BOLD}{scar.scar_id}{RESET}")
            print(f"  Spectrum: {color}{scar.spectrum.value}{RESET}")
            print(f"  Load Bar: {color}[{load_bar}]{RESET} ({scar.contradiction_degree:.2f}/10.0)")
            print(f"  Capacity: {scar.load_bearing_capacity:.3f} ln(1 + 10*load)")
            print(f"  Prop    : {scar.proposition_p[:65]}...")
            
            # Branch J: Ritual Interpretation
            omens = RitualEngine.interpret_event("scar_upsert", {
                "instance_id": scar.scar_id,
                "contradiction_degree": scar.contradiction_degree,
                "spectrum": scar.spectrum.value
            })
            for omen in omens:
                print(f"    \033[33m{omen}\033[0m")
            print(f"  {'~'*65}\n")

    def render_tension_flow_ascii(self):
        print(f"{BOLD}[TOPOLOGICAL TENSION FLOW MAP]{RESET}\n")
        scars = self.simulation.buffer.harmonic_scars
        if len(scars) < 2:
            print("  (Minimum 2 nodes required for tension flow graph)")
            return

        print("  (A-Field Singularity)")
        print("          │")
        for i, scar in enumerate(scars):
            color = ANSI_SPECTRAL_MAP.get(scar.spectrum, RESET)
            connector = "└───" if i == len(scars) - 1 else "├───"
            print(f"  {connector} [{color}{scar.scar_id}{RESET}] ══ tension flow ({scar.contradiction_degree:.1f}) ══> [Obsidian Anchor]")

    def display(self):
        self.render_header()
        self.render_scar_nodes()
        self.render_tension_flow_ascii()
        print(f"\n{BOLD}{'='*72}{RESET}\n")


def run_dashboard():
    parser = argparse.ArgumentParser(description="Cathedral-Engine CLI Dashboard")
    parser.add_argument("--watch", action="store_true", help="Continuously refresh the dashboard every 2 seconds")
    parser.add_argument("--refresh", type=int, default=2, help="Refresh interval in seconds when in watch mode")
    args = parser.parse_args()

    sim = CathedralEngineSimulation()
    archive_store = ArchiveStore()
    mapper = AshArchiveMapper(buffer=sim.buffer)

    # Load persisted state from SQLite
    saved_scars = archive_store.get_all_scars()
    for scar in saved_scars:
        sim.buffer.evaluate_contradiction(
            proposition=scar["proposition_p"],
            paradox_load=scar["contradiction_degree"],
            spectrum=SpectrumConstant(scar["spectrum"])
        )

    # Ingest default test verse pair if buffer empty
    if not sim.buffer.harmonic_scars:
        mapper.ingest_verse_pair(
            "Luminous emotional organization induces inward gravitational curvature.",
            "Gravitational curvature attenuates luminous emotional organization.",
            "IM-XII-01"
        )
        mapper.ingest_verse_pair(
            "The scar bears the permanent physical load of opposing truths.",
            "The scar dissolves logical friction into ambient void.",
            "IM-XI-02"
        )

    dashboard = CLIGraphDashboard(mapper=mapper, simulation=sim)

    if args.watch:
        try:
            while True:
                os.system("clear" if os.name != "nt" else "cls")
                dashboard.display()
                time.sleep(args.refresh)
        except KeyboardInterrupt:
            print("\nDashboard closed.")
    else:
        dashboard.display()


if __name__ == "__main__":
    run_dashboard()
