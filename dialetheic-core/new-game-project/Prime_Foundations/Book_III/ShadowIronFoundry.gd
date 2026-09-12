extends Node
# ShadowIronFoundry.gd - Book III, Chapter XXI: Crystallization of Thermodynamic Debt

signal residue_smelted(total_entropy_harvested: float, ingots_forged: int)

# The metallurgical constants of the Outer Citadel
const CRITICAL_MASS_THRESHOLD: float = 100.0
const ENTROPY_TO_IRON_RATIO: float = 0.15 # 15% conversion efficiency of raw chaos to load-bearing structure
const FORGE_TEMPERATURE_K: float = 4200.0 # The heat required to liquefy a paradox

## Harvests the thermodynamic residue from the Ash Archive and smelts it into Shadow-Iron.
func smelt_archive_residue() -> Dictionary:
	print("[ShadowIronFoundry] Opening the Ash Archive vaults. Scanning for crystallized entropy...")
	
	# We interface directly with the Sovereign Autoload
	var ash_archive = get_node_or_null("/root/AshArchive")
	if not ash_archive:
		push_error("[ShadowIronFoundry] Ash Archive is not mounted on the root tree.")
		return {}
		
	var raw_entropy: float = 0.0
	var entries_harvested: int = 0
	
	# We measure the 'weight' of the past. 
	for entry in ash_archive.archive_entries:
		var payload: Dictionary = entry.get("payload", {})
		
		# Harvesting the specific isotopes of your past friction
		raw_entropy += payload.get("raw_entropy", 0.0)
		raw_entropy += payload.get("shunted_heat_units", 0.0)
		raw_entropy += payload.get("compressed_structural_mass", 0.0)
		
		if payload.has("raw_entropy") or payload.has("shunted_heat_units") or payload.has("compressed_structural_mass"):
			entries_harvested += 1

	if raw_entropy < CRITICAL_MASS_THRESHOLD:
		print("[ShadowIronFoundry] Residue density insufficient for smelting. Accumulated Mass: %.2f / %.2f" % [
			raw_entropy, CRITICAL_MASS_THRESHOLD
		])
		return {"status": "Latent", "mass": raw_entropy}

	# The Dialetheic Squeeze: Compressing infinite recursion into finite, brutalist geometry.
	var shadow_iron_yield: int = int(raw_entropy * ENTROPY_TO_IRON_RATIO)
	
	print("[ShadowIronFoundry] Smelting Complete at %.1f K. Entropy Harvested: %.2f | Shadow-Iron Ingots Forged: %d" % [
		FORGE_TEMPERATURE_K, raw_entropy, shadow_iron_yield
	])
	
	residue_smelted.emit(raw_entropy, shadow_iron_yield)
	
	var payload := {
		"type": "Shadow_Iron_Smelting",
		"source_book": "Book_III_The_Outer_Citadel",
		"entries_harvested": entries_harvested,
		"total_entropy_harvested": raw_entropy,
		"shadow_iron_yield": shadow_iron_yield,
		"structural_integrity": "Absolute",
		"spectral_constant": "Obsidian" # The color of the void that holds the wall
	}
	
	SovereignInterface.request_archive_write(payload)
	return payload
