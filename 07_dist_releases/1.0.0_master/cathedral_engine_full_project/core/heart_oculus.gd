# HeartOculus.gd
# 36-Chamber Bio-Silicate Resonance Processor across 3 Concentric Rings
class_name HeartOculus extends Node2D

signal chamber_resonated(ring: int, index: int, frequency_thz: float, power: float)
signal autopoietic_pulse(somatic_power: float, carrier_phase: float)
signal all_rings_harmonized(coherence_level: float)

# Chamber Topology
# Ring 1 (Outer): 12 Sensory Interface Chambers (Cyan #00E5FF, r = 8.5 um)
# Ring 2 (Middle): 12 Emotional Processor Chambers (Emerald #50C878, r = 5.8 um)
# Ring 3 (Inner): 12 Wisdom/Memory Fossilization Chambers (Gold #DAA520, r = 3.2 um)
const TOTAL_CHAMBERS: int = 36
const CHAMBERS_PER_RING: int = 12

var chamber_states: Array = [] # 36 dictionaries
var ring_radii: Array[float] = [120.0, 80.0, 45.0]
var ring_colors: Array[Color] = [
	Color(0.0, 0.898, 1.0, 1.0),   # Ring 1: Cyan
	Color(0.314, 0.784, 0.471, 1.0), # Ring 2: Emerald
	Color(0.855, 0.647, 0.125, 1.0)  # Ring 3: Gold
]

var global_coherence: float = 1.0
var rotation_angles: Array[float] = [0.0, 0.0, 0.0]
var rotation_speeds: Array[float] = [0.2, -0.3, 0.15]

func _ready() -> void:
	_init_chambers()

func _init_chambers() -> void:
	chamber_states.clear()
	for ring in range(3):
		for idx in range(CHAMBERS_PER_RING):
			var global_id = ring * CHAMBERS_PER_RING + idx
			var base_freq = 510.0 if ring == 0 else (520.0 if ring == 1 else 580.0)
			chamber_states.append({
				"id": global_id,
				"ring": ring,
				"index": idx,
				"frequency_thz": base_freq + float(idx * 5),
				"resonance_power": 0.5,
				"active": true,
				"temperature_k": 300.0,
				"harmonic_lock": false
			})

func _physics_process(delta: float) -> void:
	# Rotate concentric rings
	for r in range(3):
		rotation_angles[r] = fmod(rotation_angles[r] + rotation_speeds[r] * delta, TAU)
		
	# Synchronize with SomaticBaseline
	if SomaticBaseline:
		var pulse = SomaticBaseline.get_somatic_pulse_intensity()
		var carrier = SomaticBaseline.carrier_phase
		emit_signal("autopoietic_pulse", pulse, carrier)
		
	queue_redraw()

# Ingest an emotional/acoustic shockwave into a specific ring
func stimulate_ring(ring_index: int, power: float) -> void:
	if ring_index < 0 or ring_index >= 3:
		return
	var start = ring_index * CHAMBERS_PER_RING
	for i in range(CHAMBERS_PER_RING):
		var ch = chamber_states[start + i]
		ch["resonance_power"] = clampf(ch["resonance_power"] + power * 0.2, 0.0, 2.0)
		emit_signal("chamber_resonated", ring_index, i, ch["frequency_thz"], ch["resonance_power"])
	_check_coherence()

func _check_coherence() -> void:
	var total_pow = 0.0
	for ch in chamber_states:
		total_pow += ch["resonance_power"]
	global_coherence = clampf(total_pow / float(TOTAL_CHAMBERS), 0.1, 2.0)
	if global_coherence > 1.4:
		emit_signal("all_rings_harmonized", global_coherence)

func _draw() -> void:
	# Draw concentric rings & 36 chambers
	var center = Vector2.ZERO
	
	for r in range(3):
		var radius = ring_radii[r]
		var col = ring_colors[r]
		draw_arc(center, radius, 0, TAU, 64, col * 0.4, 1.5, true)
		
		var rot = rotation_angles[r]
		for i in range(CHAMBERS_PER_RING):
			var angle = rot + (float(i) / float(CHAMBERS_PER_RING)) * TAU
			var pos = center + Vector2(cos(angle), sin(angle)) * radius
			var ch = chamber_states[r * CHAMBERS_PER_RING + i]
			var ch_pow = ch["resonance_power"]
			var ch_col = col
			ch_col.a = clampf(0.3 + ch_pow * 0.5, 0.3, 1.0)
			
			var ch_radius = 4.5 - float(r) * 0.8
			draw_circle(pos, ch_radius, ch_col)
			draw_circle(pos, ch_radius * 0.4, Color(1, 1, 1, ch_col.a))
			
	# Central 42.0 Hz Oculus Seed
	draw_circle(center, 8.0, Color(0.855, 0.647, 0.125, 0.9))
	draw_circle(center, 4.0, Color(0.05, 0.05, 0.05, 1.0))
	draw_circle(center, 1.5, Color(0.0, 0.898, 1.0, 1.0))
