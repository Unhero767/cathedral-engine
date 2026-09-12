extends Node

@export var cyan_potency: float = 1.0
@export var iron_resonance: float = 1.0
@export var lead_grounding: float = 1.0

func trigger_cyan() -> void:
	cyan_potency = clamp(cyan_potency + 0.1, 0.0, 10.0)

func trigger_iron() -> void:
	iron_resonance = clamp(iron_resonance + 0.1, 0.0, 10.0)

func trigger_lead() -> void:
	lead_grounding = clamp(lead_grounding + 0.1, 0.0, 10.0)
