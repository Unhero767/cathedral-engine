#!/usr/bin/env python3
"""
Cathedral-Engine: Outer Choirs Macro World Engine & Strategic Foresight CLI
Strata: Books XXI-XXX (Outer Choirs)
Axiom: Emotion = Physics = Biology = Architecture
"""

from __future__ import annotations
import sys
import os
import time
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
import numpy as np

# ANSI Terminal Styling
class TermColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Standard Foreground
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright
    B_RED = "\033[91m"
    B_GREEN = "\033[92m"
    B_YELLOW = "\033[93m"
    B_BLUE = "\033[94m"
    B_MAGENTA = "\033[95m"
    B_CYAN = "\033[96m"
    B_WHITE = "\033[97m"
    
    # Backgrounds
    BG_DARK = "\033[40m"
    BG_TEAL = "\033[46m"
    BG_RED = "\033[41m"

class SpectralConstant(Enum):
    GOLD = ("Joy / Radiance", TermColor.B_YELLOW, 580)
    TEAL = ("Curiosity / Inquiry", TermColor.B_CYAN, 495)
    RED = ("Anger / Conflict", TermColor.B_RED, 650)
    BLUE = ("Sorrow / Stasis", TermColor.B_BLUE, 470)
    VIOLET = ("Fear / Entropy", TermColor.B_MAGENTA, 400)
    EMERALD = ("Love / Symbiosis", TermColor.B_GREEN, 530)
    NULL = ("Obsidian / Void", TermColor.DIM + TermColor.WHITE, 0)

    def __init__(self, description: str, color_code: str, wavelength: int):
        self.description = description
        self.color_code = color_code
        self.wavelength = wavelength

    def format_badge(self) -> str:
        return f"{self.color_code}[{self.name} : {self.description}]{TermColor.RESET}"

@dataclass(frozen=True)
class MacroTrendVector:
    political_tension: float      # \tau_pol  [0.0, 1.0]
    resource_depletion: float     # \rho_res  [0.0, 1.0]
    faction_drift: float          # \delta_fac [0.0, 1.0]
    systemic_coherence: float     # \sigma_coh [0.0, 1.0]

    def to_array(self) -> np.ndarray:
        return np.array([
            self.political_tension,
            self.resource_depletion,
            self.faction_drift,
            self.systemic_coherence
        ], dtype=np.float64)

    @classmethod
    def from_array(cls, arr: np.ndarray) -> MacroTrendVector:
        clamped = np.clip(arr, 0.0, 1.0)
        return cls(float(clamped[0]), float(clamped[1]), float(clamped[2]), float(clamped[3]))

    def apply_delta(self, delta: MacroTrendVector) -> MacroTrendVector:
        return MacroTrendVector.from_array(self.to_array() + delta.to_array())

@dataclass
class WorldEra:
    epoch_id: int
    name: str
    dominant_spectrum: SpectralConstant
    lore_manifest: str
    base_modifiers: Dict[str, float] = field(default_factory=dict)

@dataclass
class MacroEvent:
    event_id: str
    title: str
    spectral_alignment: SpectralConstant
    trend_delta: MacroTrendVector
    probability_weight: float
    description: str

@dataclass
class LeverageIntervention:
    intervention_id: str
    name: str
    cost_description: str
    spectral_focus: SpectralConstant
    vector_modifier: MacroTrendVector
    description: str

@dataclass
class ScenarioNode:
    node_id: str
    turn: int
    parent_id: Optional[str]
    state_vector: MacroTrendVector
    active_era: WorldEra
    triggering_event: Optional[MacroEvent]
    probability: float
    children_ids: List[str] = field(default_factory=list)

class MacroHorizonScanner:
    """Detects emerging weak signals and generates candidate macro events."""
    def scan_signals(self, trends: MacroTrendVector) -> List[MacroEvent]:
        candidates: List[MacroEvent] = []
        
        # High tension triggers conflict signals
        if trends.political_tension > 0.60:
            candidates.append(MacroEvent(
                event_id="evt_schism_mobilization",
                title="Choir Garrison Mobilization",
                spectral_alignment=SpectralConstant.RED,
                trend_delta=MacroTrendVector(0.08, 0.03, 0.06, -0.05),
                probability_weight=min(1.0, trends.political_tension * 1.1),
                description="Outer Choir fortifications lock down transit arches as ideological disputes boil over."
            ))
        elif trends.political_tension < 0.35:
            candidates.append(MacroEvent(
                event_id="evt_concordat_accord",
                title="Concordat Trade Accords",
                spectral_alignment=SpectralConstant.EMERALD,
                trend_delta=MacroTrendVector(-0.06, -0.04, -0.05, 0.07),
                probability_weight=0.75,
                description="Regional assemblies ratify joint transit agreements across liturgical borders."
            ))

        # Resource depletion triggers scarcity crises
        if trends.resource_depletion > 0.55:
            candidates.append(MacroEvent(
                event_id="evt_ash_siphon_failure",
                title="Spectral Ash Siphon Cavitation",
                spectral_alignment=SpectralConstant.VIOLET,
                trend_delta=MacroTrendVector(0.05, 0.12, 0.04, -0.08),
                probability_weight=min(1.0, trends.resource_depletion * 1.2),
                description="Atmospheric condensers collapse under load; memory crystallization drops sharply."
            ))

        # Faction drift triggers schisms or balkanization
        if trends.faction_drift > 0.65:
            candidates.append(MacroEvent(
                event_id="evt_liturgical_heresy",
                title="Sovereign Heresy Declaration",
                spectral_alignment=SpectralConstant.NULL,
                trend_delta=MacroTrendVector(0.09, 0.01, 0.10, -0.10),
                probability_weight=trends.faction_drift,
                description="A faction discards standard harmonic constants in favor of un-indexed obsidian rituals."
            ))

        # Systemic coherence triggers harmonic alignment
        if trends.systemic_coherence > 0.70:
            candidates.append(MacroEvent(
                event_id="evt_resonant_convergence",
                title="Dialetheic Resonant Convergence",
                spectral_alignment=SpectralConstant.TEAL,
                trend_delta=MacroTrendVector(-0.07, -0.05, -0.08, 0.09),
                probability_weight=trends.systemic_coherence,
                description="Buffer chambers achieve paraconsistent stability, resolving contradiction fields peacefully."
            ))
        elif trends.systemic_coherence < 0.30:
            candidates.append(MacroEvent(
                event_id="evt_structural_fracture",
                title="Cathedral Keystone Shear",
                spectral_alignment=SpectralConstant.BLUE,
                trend_delta=MacroTrendVector(0.06, 0.04, 0.07, -0.12),
                probability_weight=0.85,
                description="Micro-fractures propagate along load-bearing arches as structural memory fades."
            ))

        return candidates

class MegatrendEngine:
    """Manages epoch state attractors and spectral constant regime shifts."""
    
    ERAS = [
        WorldEra(
            epoch_id=1,
            name="Era of Inquiry & Genesis",
            dominant_spectrum=SpectralConstant.TEAL,
            lore_manifest="The Outer Choirs harmonize under open inquiry; spectral flow is stable.",
            base_modifiers={"research_speed": 1.25, "combat_lethality": 0.8, "coherence_gain": 1.1}
        ),
        WorldEra(
            epoch_id=2,
            name="Era of the Obsidian Schism",
            dominant_spectrum=SpectralConstant.RED,
            lore_manifest="Kinetic friction ruptures the arches. Paraconsistent buffers face severe thermal load.",
            base_modifiers={"research_speed": 0.7, "combat_lethality": 1.5, "coherence_decay": 1.3}
        ),
        WorldEra(
            epoch_id=3,
            name="Era of Aetherial Depletion",
            dominant_spectrum=SpectralConstant.VIOLET,
            lore_manifest="Entropy encroaches on the reservoirs. Ash condensation drops to critical thresholds.",
            base_modifiers={"resource_burn": 1.6, "trade_friction": 1.4, "sanity_drain": 1.3}
        ),
        WorldEra(
            epoch_id=4,
            name="Era of Harmonic Synthesis",
            dominant_spectrum=SpectralConstant.GOLD,
            lore_manifest="The Cathedral achieves radiant equilibrium; all contradictions integrated into the Ash Archive.",
            base_modifiers={"all_efficiencies": 1.4, "buffer_stability": 1.8, "decay_suppression": 2.0}
        )
    ]

    def evaluate_era(self, current_era: WorldEra, trends: MacroTrendVector) -> WorldEra:
        if trends.political_tension > 0.70 and trends.faction_drift > 0.65:
            return self.ERAS[1] # Obsidian Schism
        elif trends.resource_depletion > 0.75:
            return self.ERAS[2] # Aetherial Depletion
        elif trends.systemic_coherence > 0.75 and trends.political_tension < 0.35:
            return self.ERAS[3] # Harmonic Synthesis
        elif current_era.epoch_id != 1 and trends.systemic_coherence > 0.50 and trends.political_tension < 0.50:
            return self.ERAS[0] # Return to Inquiry
        return current_era

class StrategicForesightEngine:
    """Core simulation orchestrator integrating horizon scans, scenario trees, and interventions."""
    
    def __init__(self):
        self.scanner = MacroHorizonScanner()
        self.megatrends = MegatrendEngine()
        
        # Initial State
        self.turn = 0
        self.current_era = self.megatrends.ERAS[0]
        self.current_trends = MacroTrendVector(
            political_tension=0.42,
            resource_depletion=0.38,
            faction_drift=0.35,
            systemic_coherence=0.68
        )
        self.scenario_graph: Dict[str, ScenarioNode] = {}
        self.history: List[Tuple[int, MacroTrendVector, WorldEra, Optional[str]]] = []
        self._rebuild_scenario_graph()
        self._record_history("Genesis State Initialized")

    def _rebuild_scenario_graph(self, depth: int = 2):
        self.scenario_graph.clear()
        root = ScenarioNode(
            node_id="root_curr",
            turn=self.turn,
            parent_id=None,
            state_vector=self.current_trends,
            active_era=self.current_era,
            triggering_event=None,
            probability=1.0
        )
        self.scenario_graph[root.node_id] = root
        self._expand_scenario_tree(root.node_id, depth)

    def _expand_scenario_tree(self, parent_id: str, depth: int):
        if depth <= 0 or parent_id not in self.scenario_graph:
            return

        parent = self.scenario_graph[parent_id]
        events = self.scanner.scan_signals(parent.state_vector)

        if not events:
            drift = parent.state_vector.to_array() + np.array([0.015, 0.02, 0.01, -0.01])
            next_trends = MacroTrendVector.from_array(drift)
            next_era = self.megatrends.evaluate_era(parent.active_era, next_trends)
            child_id = f"{parent.node_id}_base"
            child = ScenarioNode(
                node_id=child_id,
                turn=parent.turn + 1,
                parent_id=parent.node_id,
                state_vector=next_trends,
                active_era=next_era,
                triggering_event=None,
                probability=parent.probability * 0.90
            )
            self.scenario_graph[child_id] = child
            parent.children_ids.append(child_id)
            self._expand_scenario_tree(child_id, depth - 1)
            return

        total_weight = sum(e.probability_weight for e in events) or 1.0
        for idx, event in enumerate(events):
            new_vec = parent.state_vector.to_array() + event.trend_delta.to_array()
            next_trends = MacroTrendVector.from_array(new_vec)
            next_era = self.megatrends.evaluate_era(parent.active_era, next_trends)
            
            branch_prob = parent.probability * (event.probability_weight / total_weight)
            child_id = f"{parent.node_id}_b{idx}_{event.event_id}"
            child = ScenarioNode(
                node_id=child_id,
                turn=parent.turn + 1,
                parent_id=parent.node_id,
                state_vector=next_trends,
                active_era=next_era,
                triggering_event=event,
                probability=branch_prob
            )
            self.scenario_graph[child_id] = child
            parent.children_ids.append(child_id)
            self._expand_scenario_tree(child_id, depth - 1)

    def _record_history(self, log_msg: str):
        self.history.append((self.turn, self.current_trends, self.current_era, log_msg))

    def get_interventions(self) -> List[LeverageIntervention]:
        return [
            LeverageIntervention(
                intervention_id="inv_1_diplomacy",
                name="Liturgical Concordat Envoy",
                cost_description="15% Energy Reserves",
                spectral_focus=SpectralConstant.EMERALD,
                vector_modifier=MacroTrendVector(-0.14, 0.04, -0.12, 0.08),
                description="Dispatches neutral choir arbiters to dampen political polarization and faction drift."
            ),
            LeverageIntervention(
                intervention_id="inv_2_ash_infusion",
                name="Ash Archive Siphon Overcharge",
                cost_description="20% Buffer Resilience",
                spectral_focus=SpectralConstant.GOLD,
                vector_modifier=MacroTrendVector(0.02, -0.18, 0.01, -0.05),
                description="Vents stored memory vapor into atmospheric condensers, immediately easing resource depletion."
            ),
            LeverageIntervention(
                intervention_id="inv_3_buffer_realign",
                name="Dialetheic Buffer Recalibration",
                cost_description="10% Kinetic Output",
                spectral_focus=SpectralConstant.TEAL,
                vector_modifier=MacroTrendVector(-0.06, 0.02, -0.08, 0.16),
                description="Re-tunes paraconsistent contradiction dampers, boosting Cathedral systemic coherence."
            ),
            LeverageIntervention(
                intervention_id="inv_4_fortify",
                name="Outer Buttress Kinetic Fortification",
                cost_description="25% Aether Supply",
                spectral_focus=SpectralConstant.RED,
                vector_modifier=MacroTrendVector(0.12, 0.08, -0.04, 0.10),
                description="Hardens perimeter battlements against catastrophic collapse at the expense of regional tension."
            )
        ]

    def advance_turn(self, selected_intervention: Optional[LeverageIntervention] = None) -> str:
        self.turn += 1
        log_lines = []
        
        # 1. Apply Intervention
        if selected_intervention:
            self.current_trends = self.current_trends.apply_delta(selected_intervention.vector_modifier)
            log_lines.append(f"Applied Leverage Intervention: {selected_intervention.name}")

        # 2. Sample Horizon Events
        candidates = self.scanner.scan_signals(self.current_trends)
        triggered_event = None
        if candidates:
            weights = [c.probability_weight for c in candidates]
            total_w = sum(weights)
            probs = [w / total_w for w in weights]
            triggered_event = np.random.choice(candidates, p=probs)
            self.current_trends = self.current_trends.apply_delta(triggered_event.trend_delta)
            log_lines.append(f"Macro Horizon Event Triggered: {triggered_event.title}")
        else:
            drift = MacroTrendVector(0.015, 0.02, 0.01, -0.01)
            self.current_trends = self.current_trends.apply_delta(drift)
            log_lines.append("Ambient epochal drift applied.")

        # 3. Evaluate Megatrend / Era Shift
        new_era = self.megatrends.evaluate_era(self.current_era, self.current_trends)
        if new_era.epoch_id != self.current_era.epoch_id:
            log_lines.append(f"*** MEGATREND SHIFT *** Transitioned to [{new_era.name}] ({new_era.dominant_spectrum.name})")
            self.current_era = new_era

        # 4. Rebuild Scenario Graph for strategic foresight
        self._rebuild_scenario_graph(depth=2)
        summary_log = " | ".join(log_lines)
        self._record_history(summary_log)
        return summary_log

# UI Rendering Helpers
def render_gauge(label: str, value: float, length: int = 24, reverse_danger: bool = False) -> str:
    filled = int(round(value * length))
    filled = max(0, min(length, filled))
    empty = length - filled
    
    if not reverse_danger:
        if value < 0.40:
            c = TermColor.B_GREEN
        elif value < 0.70:
            c = TermColor.B_YELLOW
        else:
            c = TermColor.B_RED
    else:
        if value > 0.65:
            c = TermColor.B_GREEN
        elif value > 0.35:
            c = TermColor.B_YELLOW
        else:
            c = TermColor.B_RED

    bar = f"{c}{'█' * filled}{TermColor.DIM}{'░' * empty}{TermColor.RESET}"
    return f"{label:<22} [{bar}] {c}{value*100:>5.1f}%{TermColor.RESET}"

def render_dashboard(engine: StrategicForesightEngine):
    os.system('clear' if os.name == 'posix' else 'cls')
    t = engine.current_trends
    era = engine.current_era
    spec = era.dominant_spectrum
    
    print(f"{TermColor.BOLD}{TermColor.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗{TermColor.RESET}")
    print(f"{TermColor.BOLD}{TermColor.CYAN}║     CATHEDRAL-ENGINE : STRATEGIC FORESIGHT & MACRO WORLD ENGINE (CHAMBERS XXI-XXX)║{TermColor.RESET}")
    print(f"{TermColor.BOLD}{TermColor.CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝{TermColor.RESET}")
    
    print(f" {TermColor.BOLD}Turn/Epoch:{TermColor.RESET} {engine.turn:<6} | {TermColor.BOLD}Active Era:{TermColor.RESET} {era.name} (Epoch {era.epoch_id})")
    print(f" {TermColor.BOLD}Spectral Dominant:{TermColor.RESET} {spec.format_badge()} | {TermColor.DIM}{spec.wavelength}nm resonance{TermColor.RESET}")
    print(f" {TermColor.DIM}Manifest: {era.lore_manifest}{TermColor.RESET}")
    print(f"{TermColor.CYAN}──────────────────────────────────────────────────────────────────────────────────{TermColor.RESET}")
    
    print(f"{TermColor.BOLD}MACRO TREND VECTORS (\\vec{{V}}):{TermColor.RESET}")
    print("  " + render_gauge("Political Tension (τ)", t.political_tension, 22, reverse_danger=False))
    print("  " + render_gauge("Resource Depletion (ρ)", t.resource_depletion, 22, reverse_danger=False))
    print("  " + render_gauge("Faction Drift (δ)", t.faction_drift, 22, reverse_danger=False))
    print("  " + render_gauge("Systemic Coherence (σ)", t.systemic_coherence, 22, reverse_danger=True))
    print(f"{TermColor.CYAN}──────────────────────────────────────────────────────────────────────────────────{TermColor.RESET}")

    signals = engine.scanner.scan_signals(t)
    print(f"{TermColor.BOLD}HORIZON SCANNER (WEAK SIGNALS DETECTED):{TermColor.RESET}")
    if not signals:
        print(f"  {TermColor.DIM}No critical threshold signals detected. Ambient drift within nominal tolerance.{TermColor.RESET}")
    else:
        for s in signals:
            prob_pct = int(s.probability_weight * 100)
            print(f"  {s.spectral_alignment.color_code}▶ [{s.title}]{TermColor.RESET} (P={prob_pct}%) - {s.description}")
    print(f"{TermColor.CYAN}──────────────────────────────────────────────────────────────────────────────────{TermColor.RESET}")

def render_scenario_tree(engine: StrategicForesightEngine):
    print(f"{TermColor.BOLD}{TermColor.YELLOW}═══ PRE-RENDERED SCENARIO BRANCHING GRAPH (FORESIGHT HORIZON: +2 TURNS) ═══{TermColor.RESET}")
    root = engine.scenario_graph.get("root_curr")
    if not root:
        print("Scenario graph unavailable.")
        return

    def print_node(node_id: str, prefix: str = "", is_last: bool = True):
        node = engine.scenario_graph.get(node_id)
        if not node:
            return
        
        connector = "└── " if is_last else "├── "
        ev_str = f"{node.triggering_event.title}" if node.triggering_event else "Baseline Drift"
        spec_badge = node.active_era.dominant_spectrum.format_badge()
        prob_str = f"{TermColor.B_WHITE}{node.probability*100:>4.1f}%{TermColor.RESET}"
        
        v = node.state_vector
        v_summary = f"[τ:{v.political_tension:.2f} ρ:{v.resource_depletion:.2f} δ:{v.faction_drift:.2f} σ:{v.systemic_coherence:.2f}]"
        
        if node.turn == engine.turn:
            print(f"{prefix}[CURRENT T:{node.turn}] {node.active_era.name} {v_summary}")
        else:
            print(f"{prefix}{connector}[T+{node.turn - engine.turn} | P:{prob_str}] {ev_str} -> {spec_badge} {TermColor.DIM}{v_summary}{TermColor.RESET}")
        
        new_prefix = prefix + ("    " if is_last else "│   ")
        child_count = len(node.children_ids)
        for i, child_id in enumerate(node.children_ids):
            print_node(child_id, new_prefix, i == child_count - 1)

    print_node("root_curr")
    print(f"{TermColor.CYAN}──────────────────────────────────────────────────────────────────────────────────{TermColor.RESET}")

def run_cli_interactive():
    engine = StrategicForesightEngine()
    
    while True:
        render_dashboard(engine)
        print(f"{TermColor.BOLD}COMMAND CODES:{TermColor.RESET}")
        print(f"  {TermColor.B_CYAN}[1]{TermColor.RESET} Advance Turn (Ambient Progression)")
        print(f"  {TermColor.B_CYAN}[2]{TermColor.RESET} Inspect Scenario Branching Graph (Deep Foresight)")
        print(f"  {TermColor.B_CYAN}[3]{TermColor.RESET} Apply Leverage Intervention (Tactical Counter-Vector)")
        print(f"  {TermColor.B_CYAN}[4]{TermColor.RESET} Run Automated 10-Turn Foresight Simulation")
        print(f"  {TermColor.B_CYAN}[5]{TermColor.RESET} View Ash Archive Historical Ledger")
        print(f"  {TermColor.B_CYAN}[Q]{TermColor.RESET} Exit System")
        print()
        
        choice = input(f"{TermColor.BOLD}Cathedral:/> {TermColor.RESET}").strip().upper()
        
        if choice == '1':
            msg = engine.advance_turn()
            print(f"\n{TermColor.B_GREEN}Turn advanced.{TermColor.RESET} {msg}")
            time.sleep(0.8)
        
        elif choice == '2':
            render_scenario_tree(engine)
            input(f"\n{TermColor.DIM}Press [ENTER] to return to dashboard...{TermColor.RESET}")
        
        elif choice == '3':
            interventions = engine.get_interventions()
            print(f"\n{TermColor.BOLD}{TermColor.YELLOW}AVAILABLE LEVERAGE INTERVENTIONS:{TermColor.RESET}")
            for idx, inv in enumerate(interventions, 1):
                mod = inv.vector_modifier
                mod_str = f"Δ[τ:{mod.political_tension:+.2f}, ρ:{mod.resource_depletion:+.2f}, δ:{mod.faction_drift:+.2f}, σ:{mod.systemic_coherence:+.2f}]"
                print(f"  [{idx}] {inv.spectral_focus.color_code}{inv.name}{TermColor.RESET} ({inv.cost_description})")
                print(f"      {inv.description}")
                print(f"      {TermColor.DIM}Modifier: {mod_str}{TermColor.RESET}")
            print(f"  [C] Cancel")
            
            sub = input(f"\nSelect Intervention [1-{len(interventions)}]: ").strip().upper()
            if sub in ['1', '2', '3', '4']:
                chosen_inv = interventions[int(sub) - 1]
                msg = engine.advance_turn(selected_intervention=chosen_inv)
                print(f"\n{TermColor.B_GREEN}Intervention deployed and turn advanced!{TermColor.RESET}")
                print(msg)
                time.sleep(1.2)
            else:
                print("Intervention aborted.")
                time.sleep(0.5)

        elif choice == '4':
            print(f"\n{TermColor.YELLOW}Executing 10-turn Monte Carlo strategic foresight trajectory...{TermColor.RESET}")
            for step in range(10):
                inv_to_apply = None
                if engine.current_trends.systemic_coherence < 0.45:
                    inv_to_apply = engine.get_interventions()[2]
                elif engine.current_trends.political_tension > 0.65:
                    inv_to_apply = engine.get_interventions()[0]
                elif engine.current_trends.resource_depletion > 0.65:
                    inv_to_apply = engine.get_interventions()[1]
                
                log = engine.advance_turn(selected_intervention=inv_to_apply)
                print(f"  Turn {engine.turn:02d} | Era: {engine.current_era.dominant_spectrum.name:<7} | {log}")
                time.sleep(0.2)
            input(f"\n{TermColor.DIM}10-turn simulation cycle completed. Press [ENTER] to view dashboard...{TermColor.RESET}")

        elif choice == '5':
            print(f"\n{TermColor.BOLD}{TermColor.CYAN}═══ ASH ARCHIVE HISTORICAL LEDGER (NEVER-OVERWRITE) ═══{TermColor.RESET}")
            for item in engine.history:
                turn_no, trends, era_obj, log_txt = item
                t_arr = trends.to_array()
                print(f"  T:{turn_no:02d} | {era_obj.dominant_spectrum.name:<7} | [τ:{t_arr[0]:.2f} ρ:{t_arr[1]:.2f} δ:{t_arr[2]:.2f} σ:{t_arr[3]:.2f}] | {log_txt}")
            print(f"{TermColor.CYAN}──────────────────────────────────────────────────────────────────────────────────{TermColor.RESET}")
            input(f"\n{TermColor.DIM}Press [ENTER] to return to dashboard...{TermColor.RESET}")

        elif choice == 'Q':
            print(f"\n{TermColor.B_CYAN}Cathedral-Engine session suspended. Telemetry persisted to Ash Archive.{TermColor.RESET}")
            break

def run_automated_test_suite():
    print("Initializing Automated Verification for Strategic Foresight Engine...")
    engine = StrategicForesightEngine()
    
    assert engine.turn == 0
    assert engine.current_era.epoch_id == 1
    assert len(engine.scenario_graph) > 1
    print("✓ [PASS] Initial state and Scenario Branch Graph initialized.")
    
    signals = engine.scanner.scan_signals(MacroTrendVector(0.8, 0.8, 0.8, 0.2))
    assert len(signals) >= 2
    print(f"✓ [PASS] Horizon Scanner detected {len(signals)} weak signals under high entropy stress.")
    
    schism_era = engine.megatrends.evaluate_era(engine.current_era, MacroTrendVector(0.85, 0.4, 0.85, 0.2))
    assert schism_era.epoch_id == 2
    print(f"✓ [PASS] Megatrend Attractor successfully triggered transition to {schism_era.name}.")
    
    inv = engine.get_interventions()[0]
    log = engine.advance_turn(selected_intervention=inv)
    assert engine.turn == 1
    print(f"✓ [PASS] Turn cycle advanced to Turn 1 with intervention '{inv.name}'. Log: {log}")
    
    render_scenario_tree(engine)
    print("✓ [PASS] Scenario Branching DAG rendered successfully.")
    print("\nAll engine verifications passed.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_automated_test_suite()
    else:
        run_cli_interactive()
