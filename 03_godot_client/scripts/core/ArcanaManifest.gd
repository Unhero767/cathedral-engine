class_name ArcanaManifest
extends RefCounted

const LIVING_ARCANA_REGISTRY: Dictionary = {
	1: {"name": "The Sovereign Root", "zone": 1, "spectral": "Gold/Joy", "base_phi": 8.0},
	2: {"name": "The Dialetheic Mirror", "zone": 1, "spectral": "Teal/Curiosity", "base_phi": 6.5},
	3: {"name": "The Paraconsistent Gate", "zone": 1, "spectral": "Bronze-Obsidian/Null", "base_phi": 4.0},
	11: {"name": "The Pulse of Joy", "zone": 2, "spectral": "Gold/Joy", "base_phi": 9.0},
	12: {"name": "The Resonant Abyss", "zone": 2, "spectral": "Blue/Sorrow", "base_phi": 2.5},
	15: {"name": "The Vector Forge", "zone": 2, "spectral": "Teal/Curiosity", "base_phi": 7.0},
	21: {"name": "The Isomorphic Lattice", "zone": 3, "spectral": "Emerald/Love", "base_phi": 6.0},
	25: {"name": "The HD-2D Horizon", "zone": 3, "spectral": "Teal/Curiosity", "base_phi": 5.5},
	31: {"name": "The Ash Stratum", "zone": 4, "spectral": "Bronze-Obsidian/Null", "base_phi": 1.0},
	35: {"name": "The Harmonic Scar", "zone": 4, "spectral": "Red/Anger", "base_phi": 7.8},
	40: {"name": "The Block Universe", "zone": 4, "spectral": "Violet/Fear", "base_phi": 3.0}
}

static func trigger_card_activation(card_id: int) -> void:
	if not LIVING_ARCANA_REGISTRY.has(card_id):
		push_warning("Arcana Card ID not registered: %d" % card_id)
		return
		
	var card_data = LIVING_ARCANA_REGISTRY[card_id]
	if Engine.has_singleton("MLAOSBridge"):
		var bridge = Engine.get_singleton("MLAOSBridge")
		bridge.send_telemetry_tick(card_data["base_phi"])
