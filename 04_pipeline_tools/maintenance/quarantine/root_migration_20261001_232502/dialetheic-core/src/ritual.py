from typing import Dict, Any, List

MANTRAS = {
    "VIOLET": [
        "The light bends inward, organizing what cannot be spoken.",
        "Grief becomes geometry upon the altar of Ash."
    ],
    "BRONZE_OBSIDIAN": [
        "The scar accepts what the flesh refuses to carry.",
        "Obsidian does not forgive weight; it permineralizes it."
    ],
    "TEAL": [
        "A cold mercy moves through the dialectic contradiction.",
        "The wound learns to breathe within the buffer."
    ],
    "GOLD": [
        "Luminous emotional organization establishes the Plumb Line.",
        "Radial sun-vaults stabilize the local reality matrix."
    ],
    "RED": [
        "Rupture precedes the hardening of the sanctuary-flesh.",
        "The shard-forge ignites the Autopoietic Heart."
    ]
}

def generate_omens(state: dict) -> List[str]:
    omens = []
    quarantine_thresh = float(state.get("quarantine_threshold", 7.5))
    
    for scar in state.get("scars", []):
        load = float(scar.get("contradiction_degree", scar.get("paradox_load", 0.0)))
        scar_id = scar.get("scar_id", scar.get("id", "scar"))
        spectrum = scar.get("spectrum", "TEAL")

        if load >= quarantine_thresh:
            omens.append(f"⚠ QUARANTINE BREACH: {scar_id} bears a load the flesh cannot carry ({load:.2f}/{quarantine_thresh:.1f}).")
        if spectrum == "BRONZE_OBSIDIAN":
            omens.append(f"⚓ ANCHOR CONSECRATED: {scar_id} is sealed in obsidian.")

    afield = state.get("afield", {})
    flux = float(afield.get("flux", state.get("flux", 0.0)))
    if flux > 2.0:
        omens.append(f"🌪 TURBULENCE: The A-Field trembles; geometry is unstable (Flux: {flux:.2f}).")

    if not omens:
        omens.append("System initialized under Never-Overwrite Doctrine.")
        omens.append("The light bends inward, organizing what cannot be spoken.")

    return omens

class RitualEngine:
    @staticmethod
    def interpret_event(event_type: str, data: Dict[str, Any]) -> List[str]:
        omens = []
        spectrum = data.get("spectrum", "TEAL")
        load = float(data.get("paradox_load", data.get("contradiction_degree", 0.0)))
        instance_id = data.get("instance_id", "aurelia-node")

        if event_type == "scar_upsert" or event_type == "scar_created":
            if load >= 8.0:
                omens.append(f"⚓ ANCHOR CONSECRATED: Node {instance_id} has crossed paradox threshold {load:.2f}.")
                omens.append(f"⚠ QUARANTINE BREACH: {instance_id} is sealed in permanent obsidian.")
            elif load >= 5.0:
                omens.append(f"Dialetheic collision detected on {instance_id} (Load: {load:.2f}).")

            mantra_list = MANTRAS.get(spectrum, MANTRAS["TEAL"])
            omens.append(f"{mantra_list[0]}")

        elif event_type == "flux_spike":
            omens.append(f"🌪 TURBULENCE: Flux magnitude spiked to {load:.2f}.")

        return omens
