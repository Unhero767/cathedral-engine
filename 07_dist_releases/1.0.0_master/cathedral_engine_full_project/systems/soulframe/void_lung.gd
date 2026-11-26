# VoidLung.gd
# Law of Re-Weaving: Trauma-to-Breath Conversion & Alveolar Pneumatics
class_name VoidLung extends Node

signal breath_changed(current_breath: float, max_breath: float)
signal trauma_reweaved(trauma_amount: float, converted_breath: float)
signal pulmonary_exhaustion()

@export var max_breath: float = 100.0
@export var breath_recovery_rate: float = 12.0
@export var trauma_conversion_efficiency: float = 0.85

var current_breath: float = 100.0
var accumulated_trauma: float = 0.0
var is_reweaving: bool = false

func _physics_process(delta: float) -> void:
	if current_breath < max_breath:
		# Passive autopoietic regeneration synced with Somatic Baseline
		var compliance = 1.0
		if SomaticBaseline:
			compliance = SomaticBaseline.ALVEOLAR_COMPLIANCE_KPA
		current_breath = minf(max_breath, current_breath + (breath_recovery_rate * compliance) * delta)
		emit_signal("breath_changed", current_breath, max_breath)

# Consumes breath for maneuvers or arcana casting
func consume_breath(amount: float) -> bool:
	if current_breath >= amount:
		current_breath -= amount
		emit_signal("breath_changed", current_breath, max_breath)
		return true
	emit_signal("pulmonary_exhaustion")
	return false

# Ingest kinetic or entropy damage and convert into usable breath stamina
func ingest_trauma(damage_amount: float) -> float:
	accumulated_trauma += damage_amount
	var converted = damage_amount * trauma_conversion_efficiency
	current_breath = minf(max_breath, current_breath + converted)
	
	emit_signal("trauma_reweaved", damage_amount, converted)
	emit_signal("breath_changed", current_breath, max_breath)
	
	if AshArchive:
		AshArchive.commit_entry({
			"event": "TRAUMA_REWEAVED",
			"raw_trauma": damage_amount,
			"converted_breath": converted,
			"remaining_breath": current_breath
		}, ["SOULFRAME", "VOID_LUNG"])
		
	return converted
