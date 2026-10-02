extends Node
class_name SomaticHeatSink

## MLAOS SUBSTRATE — Somatic HeatSink
## Thermodynamic confessor of the Iron Shadow Foundry.
##
## Absorbs waste heat, dissipates it over time,
## and records saturation events to the Ash Archive.
##
## Spectral Constant: Teal


# --- Canonical Thermal Constants ---

const MAX_HEAT_CAPACITY := 500.0
const BASE_DISSIPATION_RATE := 25.0
const QUENCH_HEAT_CONVERSION := 40.0

const SATURATION_WARN := 0.75
const SATURATION_CRIT := 0.95

const EMERGENCY_VENT_FACTOR := 0.5
const VENT_FATIGUE_COST := 0.05
const RECOVERY_RATE := 0.01


# --- Signals ---

signal heat_absorbed(amount, stored, capacity)
signal saturated(stored)
signal vented(amount_removed, fatigue)


# --- HeatSink State ---

var stored_heat: float = 0.0
var somatic_fatigue: float = 0.0

var total_heat_absorbed: float = 0.0
var total_heat_dissipated: float = 0.0
var total_quench_load: float = 0.0

var _was_saturated: bool = false


func _process(delta: float) -> void:
	# Passive thermal dissipation.
	if stored_heat > 0.0:
		var removed := min(
			stored_heat,
			get_dissipation_rate() * delta
		)

		stored_heat -= removed
		total_heat_dissipated += removed

	# Slow somatic recovery.
	if somatic_fatigue > 0.0:
		somatic_fatigue = max(
			0.0,
			somatic_fatigue - RECOVERY_RATE * delta
		)

	# Clear saturation latch when safely below critical.
	if _was_saturated and get_saturation() < SATURATION_CRIT:
		_was_saturated = false


func get_state() -> String:
	var saturation := get_saturation()

	if saturation >= SATURATION_CRIT or stored_heat >= MAX_HEAT_CAPACITY:
		return "SATURATED"

	if saturation >= SATURATION_WARN:
		return "STRAINED"

	return "NOMINAL"


func get_saturation() -> float:
	return clamp(stored_heat / MAX_HEAT_CAPACITY, 0.0, 1.0)


func get_absorption_efficiency() -> float:
	# Absorption becomes less confident as the HeatSink fills.
	return clamp(1.0 - get_saturation() * 0.8, 0.1, 1.0)


func get_dissipation_rate() -> float:
	# Fatigue makes the body less able to shed heat.
	return BASE_DISSIPATION_RATE * (1.0 - somatic_fatigue * 0.5)


func absorb_heat(amount: float) -> float:
	if amount <= 0.0:
		return 0.0

	var available := max(0.0, MAX_HEAT_CAPACITY - stored_heat)

	if available <= 0.0:
		_announce_saturation()
		return 0.0

	var absorbed := min(
		amount,
		available,
		amount * get_absorption_efficiency()
	)

	if absorbed <= 0.0:
		return 0.0

	stored_heat += absorbed
	total_heat_absorbed += absorbed

	heat_absorbed.emit(absorbed, stored_heat, MAX_HEAT_CAPACITY)

	if get_saturation() >= SATURATION_CRIT:
		_announce_saturation()

	return absorbed


func receive_quench(normalized_load: float) -> void:
	if normalized_load <= 0.0:
		return

	var heat := normalized_load * QUENCH_HEAT_CONVERSION
	var available := max(0.0, MAX_HEAT_CAPACITY - stored_heat)
	var added := min(heat, available)

	stored_heat += added
	total_quench_load += normalized_load

	if get_saturation() >= SATURATION_CRIT:
		_announce_saturation()


func emergency_vent() -> float:
	var removed := stored_heat * EMERGENCY_VENT_FACTOR

	if removed <= 0.0:
		return 0.0

	stored_heat -= removed

	somatic_fatigue = min(
		1.0,
		somatic_fatigue + VENT_FATIGUE_COST
	)

	vented.emit(removed, somatic_fatigue)

	_log_event(
		"Somatic_HeatSink_Emergency_Vent",
		{
			"source": "Substrate / Somatic HeatSink",
			"heat_vented": _round2(removed),
			"remaining_heat": _round2(stored_heat),
			"somatic_fatigue": _round3(somatic_fatigue),
			"spectral_constant": "Teal",
		}
	)

	return removed


func get_status() -> Dictionary:
	return {
		"state": get_state(),
		"stored_heat": _round2(stored_heat),
		"capacity": _round2(MAX_HEAT_CAPACITY),
		"saturation": _round3(get_saturation()),
		"absorption_efficiency": _round3(get_absorption_efficiency()),
		"dissipation_rate": _round2(get_dissipation_rate()),
		"somatic_fatigue": _round3(somatic_fatigue),
		"total_heat_absorbed": _round2(total_heat_absorbed),
		"total_heat_dissipated": _round2(total_heat_dissipated),
		"total_quench_load": _round3(total_quench_load),
	}


func _announce_saturation() -> void:
	if _was_saturated:
		return

	_was_saturated = true

	saturated.emit(stored_heat)

	_log_event(
		"Somatic_HeatSink_Saturation",
		{
			"source": "Substrate / Somatic HeatSink",
			"stored_heat": _round2(stored_heat),
			"capacity": _round2(MAX_HEAT_CAPACITY),
			"saturation": _round3(get_saturation()),
			"spectral_constant": "Teal",
		}
	)


func _log_event(event: String, payload: Dictionary) -> void:
	var archive = get_node_or_null("/root/ash_archive")

	if archive and archive.has_method("append_event"):
		archive.append_event(event, payload)


func _round2(value: float) -> float:
	return round(value * 100.0) / 100.0


func _round3(value: float) -> float:
	return round(value * 1000.0) / 1000.0
