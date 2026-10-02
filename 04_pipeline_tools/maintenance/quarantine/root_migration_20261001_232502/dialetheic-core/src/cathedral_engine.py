"""
Cathedral-Engine & Omni-Codex Ω Permanent Runtime Ledger
Core State Management, Data Models, Simulation Logic, Vault Persistence, and Book II Mechanics.
Pydantic v1 & v2 Cross-Compatible.
"""

import os
import sys
import re
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
import math
from pydantic import BaseModel, Field, validator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    from src.archive_store import ArchiveStore
except ModuleNotFoundError:
    from archive_store import ArchiveStore


class SpectrumConstant(str, Enum):
    GOLD = "GOLD"
    TEAL = "TEAL"
    BLUE = "BLUE"
    RED = "RED"
    VIOLET = "VIOLET"
    EMERALD = "EMERALD"
    BRONZE_OBSIDIAN = "BRONZE_OBSIDIAN"


class OutcomeClassification(str, Enum):
    RESONANCE_KEYSTONE = "RESONANCE_KEYSTONE"
    LITHIC_MONOLITH = "LITHIC_MONOLITH"
    STROBING_SUPPRESSED = "STROBING_SUPPRESSED"


class SovereignHysteresisState(BaseModel):
    tau_alpha: float = Field(default=0.5, description="Hysteresis threshold rate tau_alpha")
    delta_t_min: float = Field(default=1.0, description="Minimum duration required for permission stabilization (seconds)")
    current_flux: float = Field(default=0.0, description="Current phi flux magnitude")
    previous_flux: float = Field(default=0.0, description="Previous phi flux magnitude")
    last_update_time: float = Field(default=0.0, description="Timestamp of last update")
    sustained_duration: float = Field(default=0.0, description="Duration for which dPhi/dt > tau_alpha")
    is_permission_active: bool = Field(default=False, description="Sovereign permission state")

    def update_flux(self, new_flux: float, current_time: float) -> OutcomeClassification:
        delta_t = current_time - self.last_update_time
        if delta_t <= 0:
            delta_t = 0.001

        dphi_dt = (new_flux - self.current_flux) / delta_t
        self.previous_flux = self.current_flux
        self.current_flux = new_flux
        self.last_update_time = current_time

        if dphi_dt > self.tau_alpha:
            self.sustained_duration += delta_t
            if self.sustained_duration >= self.delta_t_min:
                self.is_permission_active = True
                return OutcomeClassification.RESONANCE_KEYSTONE
            else:
                self.is_permission_active = False
                return OutcomeClassification.STROBING_SUPPRESSED
        else:
            self.sustained_duration = 0.0
            self.is_permission_active = False
            return OutcomeClassification.LITHIC_MONOLITH


class HarmonicScar(BaseModel):
    scar_id: str
    proposition_p: str
    contradiction_degree: float
    spectrum: SpectrumConstant
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    load_bearing_capacity: float


class DialetheicBuffer(BaseModel):
    max_paradox_capacity: float = Field(default=10.0)
    quarantine_threshold: float = Field(default=7.5)
    harmonic_scars: List[HarmonicScar] = Field(default_factory=list)

    def evaluate_contradiction(
        self, proposition: str, paradox_load: float, spectrum: SpectrumConstant, custom_scar_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if paradox_load >= self.quarantine_threshold:
            return {
                "action": "QUARANTINE",
                "spectrum": SpectrumConstant.BRONZE_OBSIDIAN,
                "paradox_load": paradox_load,
                "proposition": proposition,
            }
        else:
            scar_id = custom_scar_id or f"scar_{len(self.harmonic_scars) + 1}"
            scar = HarmonicScar(
                scar_id=scar_id,
                proposition_p=proposition,
                contradiction_degree=paradox_load,
                spectrum=spectrum,
                load_bearing_capacity=math.log1p(paradox_load * 10.0),
            )
            self.harmonic_scars.append(scar)
            return {
                "action": "HARMONIC_SCAR_FORGED",
                "scar": scar,
            }


class NodeSyncRequest(BaseModel):
    instance_id: str
    mqi_score: float = Field(..., ge=0.0, le=100.0)
    a_field_temperature_k: float = Field(..., ge=0.0)
    current_flux: float
    active_spectrum: SpectrumConstant
    active_paradox_load: float

    @validator("instance_id")
    def validate_instance_id(cls, v):
        pattern = r"^aurelia-(0[1-9]|[1-4][0-9])$"
        if not re.match(pattern, v):
            raise ValueError(f"instance_id '{v}' must match pattern 'aurelia-XX' (01-49)")
        return v


class NodeSyncResponse(BaseModel):
    instance_id: str
    status: str
    corridor_width: float
    permission_active: bool
    action_required: Optional[str] = None


class CathedralEngineSimulation:
    def __init__(self, initial_corridor_width: float = 100.0, gamma_decay: float = 0.05, store: Optional[ArchiveStore] = None):
        self.initial_width = initial_corridor_width
        self.gamma = gamma_decay
        self.a_field_temp = 300.0
        self.total_system_rpm = 77.45  # Kinetic turbine baseline
        self.hysteresis = SovereignHysteresisState(tau_alpha=0.5, delta_t_min=1.0)
        self.buffer = DialetheicBuffer()
        self.store = store or ArchiveStore()
        self.load_from_vault()

    def load_from_vault(self):
        """Resurrects state, RPM, and scars from the SQLite vault."""
        state = self.store.get_state()
        if state:
            self.a_field_temp = float(state.get("afield_temp", 300.0))
            self.hysteresis.current_flux = float(state.get("flux", 0.0))

        rpm_meta = self.store.get_meta("total_system_rpm")
        if rpm_meta:
            self.total_system_rpm = float(rpm_meta)

        saved_scars = self.store.get_scars()
        for scar_data in saved_scars:
            scar_id = scar_data.get("scar_id")
            if not any(s.scar_id == scar_id for s in self.buffer.harmonic_scars):
                load = float(scar_data.get("paradox_load", 0.0))
                capacity = float(scar_data.get("capacity") or math.log1p(load * 10.0))
                spectrum_str = scar_data.get("spectrum") or "TEAL"
                prop_text = scar_data.get("proposition_p") or scar_data.get("proposition_text") or f"[{scar_id}] Restored Scar"
                
                scar_obj = HarmonicScar(
                    scar_id=scar_id,
                    proposition_p=prop_text,
                    contradiction_degree=load,
                    spectrum=SpectrumConstant(spectrum_str),
                    load_bearing_capacity=capacity
                )
                self.buffer.harmonic_scars.append(scar_obj)

    def save_to_vault(self):
        """Seals current A-Field state into the SQLite vault."""
        self.store.save_state(
            afield_temp=self.a_field_temp,
            flux=self.hysteresis.current_flux
        )
        self.store.set_meta("total_system_rpm", str(self.total_system_rpm))

    def apply_tri_key_compression(self, scar_id: str, tension_score: float) -> Dict[str, Any]:
        """Subject scar to Tri-Key Geological Compression & kinetic yield acceleration."""
        self.total_system_rpm += tension_score
        self.save_to_vault()
        return {
            "status": "BUFFER_ENGAGED",
            "scar_id": scar_id,
            "kinetic_yield_added": tension_score,
            "total_system_rpm": self.total_system_rpm,
            "category": "TOLERABLE_FRICTION"
        }

    def calculate_corridor_width(self, spectral_friction: float) -> float:
        narrowed_width = self.initial_width * math.exp(-self.gamma * spectral_friction)
        return max(narrowed_width, 1.0)
