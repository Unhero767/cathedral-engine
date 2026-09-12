from typing import Dict, Any
from src.cathedral_engine import CathedralEngineSimulation, SpectrumConstant
from src.archive_store import ArchiveStore

class RPGDialetheicBridge:
    def __init__(self, simulation: CathedralEngineSimulation):
        self.simulation = simulation

    def process_tile_event(self, character_name: str, tile_type: str, paradox_charge: float, heat_delta: float) -> Dict[str, Any]:
        # Update A-Field temperature based on tile thermal impact
        self.simulation.a_field_temp = max(300.0, self.simulation.a_field_temp + heat_delta)

        scar_event = None
        if paradox_charge > 0.0:
            spectrum = SpectrumConstant.BRONZE_OBSIDIAN if paradox_charge >= 7.5 else SpectrumConstant.TEAL
            eval_res = self.simulation.buffer.evaluate_contradiction(
                proposition=f"[{character_name}] Stepped on {tile_type} (Paradox Charge: {paradox_charge:.2f})",
                paradox_load=paradox_charge,
                spectrum=spectrum
            )
            if "scar" in eval_res:
                scar_dict = {
                    "scar_id": eval_res["scar"].scar_id,
                    "instance_id": character_name,
                    "spectrum": spectrum.value,
                    "paradox_load": paradox_charge,
                    "capacity": eval_res["scar"].load_bearing_capacity,
                    "proposition_p": eval_res["scar"].proposition_p
                }
                self.simulation.store.upsert_scar(scar_dict)
                scar_event = scar_dict

        self.simulation.save_to_vault()

        return {
            "character_name": character_name,
            "tile_type": tile_type,
            "a_field_temp_k": self.simulation.a_field_temp,
            "paradox_charge": paradox_charge,
            "scar_forged": scar_event
        }
