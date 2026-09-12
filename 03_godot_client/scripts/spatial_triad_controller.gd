class_name SpatialTriadController
extends CharacterBody2D

## EAS-03 Spatial Triad Navigation Controller & Paraconsistent State Validator
## System Classification: MLAOS-PRIME // ARCHITECTONIC-FIELD-V4
## Prime Isomorphism Axiom: Emotion == Physics == Magic == Biology == Architecture

const CathedralAtlasBuilder = preload("res://03_godot_client/scripts/core/CathedralAtlasBuilder.gd")

# ------------------------------------------------------------------------------
# Signals
# ------------------------------------------------------------------------------
signal state_transition_committed(event_record: Dictionary)
signal dialetheic_collision_detected(coord: Vector2, resolution_type: String)
signal harmonic_scar_petrified(scar_data: Dictionary)
signal afield_kinetics_updated(radius: float, current_velocity: Vector2)
signal lumen_cadence_pulsed(gain_value: float, spectral_constant: int)
signal liturgical_animation_changed(previous_state: StringName, new_state: StringName)

# ------------------------------------------------------------------------------
# Constants & Enums
# ------------------------------------------------------------------------------
enum BelnapDunnValue {
	T = 0, # True: Sound, verified passable coordinate
	F = 1, # False: Blocked obstruction or null void
	B = 2, # Both: Dialetheic contradiction (simultaneously passable and blocked)
	N = 3  # Neither: Unmapped / Glitch-Waste unindexed space
}

enum SpectralConstant {
	THETA_GOLD = 0,      # Joy / Law (580 THz)
	PSI_TEAL = 1,        # Curiosity / Recursion (510 THz)
	DELTA_BLUE = 2,      # Sorrow / Archiving (450 THz)
	PHI_RED = 3,         # Anger / Entropy (680 THz)
	OMEGA_VIOLET = 4,    # Fear / Adaptation (720 THz)
	EPSILON_EMERALD = 5, # Love / Binding (540 THz)
	NULL_OBSIDIAN = 6    # Void / Anti-Resonance (0 THz)
}

const BASELINE_EGO_DENSITY: float = 8.3
const BASELINE_AFIELD_RADIUS: float = 64.0
const INPUT_BUFFER_SIZE: int = 16
const GENESIS_HASH: String = "0000000000000000000000000000000000000000000000000000000000000000"

# ------------------------------------------------------------------------------
# Exported Properties
# ------------------------------------------------------------------------------
@export_group("Kinesthetic Layer (Perceived Space)")
@export var base_speed: float = 140.0
@export var acceleration: float = 1200.0
@export var friction: float = 1400.0
@export var subpixel_rendering: bool = true
@export var target_camera: Camera2D
@export var camera_lookahead_distance: float = 32.0
@export var camera_smoothing_speed: float = 6.5

@export_group("State Validator (Conceived Space)")
@export var ego_density: float = 8.3
@export var active_spectral_constant: SpectralConstant = SpectralConstant.PSI_TEAL
@export var afield_beta: float = 0.42
@export var enable_metamorphic_squeeze: bool = true

@export_group("Lived Space & Visual Anchors")
@export var animated_sprite: AnimatedSprite2D
@export var master_atlas_texture: Texture2D
@export var dialogue_cadence_intensity: float = 1.0

# ------------------------------------------------------------------------------
# Internal Runtime State
# ------------------------------------------------------------------------------
var _input_buffer: Array[Dictionary] = []
var _input_frame_counter: int = 0
var _subpixel_accumulator: Vector2 = Vector2.ZERO
var _smoothed_velocity: Vector2 = Vector2.ZERO
var _camera_initial_offset: Vector2 = Vector2.ZERO
var _dialetheic_turbulence: float = 0.0
var _current_afield_radius: float = BASELINE_AFIELD_RADIUS
var _current_emotional_magnitude: float = 1.0

var _spatial_truth_matrix: Dictionary = {}
var _harmonic_scars: Array[Dictionary] = []
var _ash_archive_ledger: Array[Dictionary] = []
var _latest_block_hash: String = GENESIS_HASH

var current_liturgical_animation: StringName = &"liturgical_idle"
var _animation_lock_timer: float = 0.0

# ------------------------------------------------------------------------------
# Engine Lifecycle
# ------------------------------------------------------------------------------
func _ready() -> void:
	_initialize_input_buffer()
	_initialize_ash_archive()
	
	if target_camera:
		_camera_initial_offset = target_camera.offset
		
	if master_atlas_texture and animated_sprite:
		setup_atlas(master_atlas_texture)
	elif animated_sprite and ResourceLoader.exists("res://aurelia9_atlas_strip.png"):
		var default_tex := load("res://aurelia9_atlas_strip.png") as Texture2D
		setup_atlas(default_tex)
		
	var initial_grid := Vector2i((global_position / 16.0).floor())
	_spatial_truth_matrix[initial_grid] = BelnapDunnValue.T
	
	_commit_telemetry_event("SYSTEM_INITIALIZE", {
		"initial_position": global_position,
		"ego_density": ego_density,
		"spectral_constant": active_spectral_constant,
		"afield_radius": _current_afield_radius
	})

func setup_atlas(texture: Texture2D) -> void:
	if not texture or not animated_sprite:
		return
	master_atlas_texture = texture
	var frames: SpriteFrames = CathedralAtlasBuilder.build_sprite_frames(texture)
	animated_sprite.sprite_frames = frames
	set_liturgical_animation(&"liturgical_idle")

func set_liturgical_animation(anim_name: StringName, force_lock_duration: float = 0.0) -> void:
	if not animated_sprite or not animated_sprite.sprite_frames:
		return
	if not animated_sprite.sprite_frames.has_animation(anim_name):
		return
		
	if _animation_lock_timer > 0.0 and anim_name == &"liturgical_idle":
		return
		
	if current_liturgical_animation != anim_name:
		var prev_anim := current_liturgical_animation
		current_liturgical_animation = anim_name
		animated_sprite.play(anim_name)
		liturgical_animation_changed.emit(prev_anim, anim_name)
		
	if force_lock_duration > 0.0:
		_animation_lock_timer = force_lock_duration

func _physics_process(delta: float) -> void:
	if _animation_lock_timer > 0.0:
		_animation_lock_timer = max(0.0, _animation_lock_timer - delta)
		
	var raw_input := _poll_kinesthetic_input()
	_record_input_frame(raw_input)
	_calculate_afield_kinetics()
	_process_kinesthetic_movement(raw_input, delta)
	_process_camera_kinematics(delta)
	_update_lived_space_visuals()
	_update_animation_state(raw_input)

func _update_animation_state(input_direction: Vector2) -> void:
	if _animation_lock_timer > 0.0:
		return
		
	if input_direction.length_squared() > 0.001:
		set_liturgical_animation(&"ocular_surge")
	else:
		if ego_density > 14.0:
			set_liturgical_animation(&"harmonic_resonance")
		else:
			set_liturgical_animation(&"liturgical_idle")

# ------------------------------------------------------------------------------
# 1. Kinesthetic Layer (Perceived Space)
# ------------------------------------------------------------------------------
func _initialize_input_buffer() -> void:
	_input_buffer.clear()
	for i in range(INPUT_BUFFER_SIZE):
		_input_buffer.append({
			"frame_id": 0,
			"vector": Vector2.ZERO,
			"cadence_pulse": 0.0,
			"timestamp_usec": Time.get_ticks_usec()
		})

func _poll_kinesthetic_input() -> Vector2:
	var move_vec := Vector2.ZERO
	move_vec.x = Input.get_axis("ui_left", "ui_right")
	move_vec.y = Input.get_axis("ui_up", "ui_down")
	if move_vec.length_squared() > 1.0:
		move_vec = move_vec.normalized()
	return move_vec

func _record_input_frame(raw_vector: Vector2) -> void:
	_input_frame_counter += 1
	var buffer_index := _input_frame_counter % INPUT_BUFFER_SIZE
	_input_buffer[buffer_index] = {
		"frame_id": _input_frame_counter,
		"vector": raw_vector,
		"cadence_pulse": dialogue_cadence_intensity,
		"timestamp_usec": Time.get_ticks_usec()
	}

func _process_kinesthetic_movement(input_direction: Vector2, delta: float) -> void:
	var target_velocity := input_direction * base_speed
	
	if input_direction.length_squared() > 0.001:
		_smoothed_velocity = _smoothed_velocity.move_toward(target_velocity, acceleration * delta)
	else:
		_smoothed_velocity = _smoothed_velocity.move_toward(Vector2.ZERO, friction * delta)
		
	var proposed_displacement := _smoothed_velocity * delta
	var target_global_pos := global_position + proposed_displacement
	var target_grid_coord := Vector2i((target_global_pos / 16.0).floor())
	
	var validation_result: BelnapDunnValue = _evaluate_spatial_truth(target_grid_coord)
	
	match validation_result:
		BelnapDunnValue.T:
			velocity = _smoothed_velocity
		BelnapDunnValue.F:
			_smoothed_velocity = Vector2.ZERO
			velocity = Vector2.ZERO
		BelnapDunnValue.B:
			var resolved_velocity := _resolve_dialetheic_step(target_grid_coord, _smoothed_velocity, delta)
			velocity = resolved_velocity
		BelnapDunnValue.N:
			velocity = _smoothed_velocity * 0.35
			_crystallize_unindexed_coordinate(target_grid_coord)
			
	if subpixel_rendering:
		_subpixel_accumulator += velocity * delta
		var integer_displacement := _subpixel_accumulator.floor()
		_subpixel_accumulator -= integer_displacement
		move_and_slide()
	else:
		move_and_slide()
		
	afield_kinetics_updated.emit(_current_afield_radius, velocity)

func _process_camera_kinematics(delta: float) -> void:
	if not target_camera:
		return
		
	var lookahead_target := _smoothed_velocity.normalized() * camera_lookahead_distance
	if _smoothed_velocity.length_squared() < 1.0:
		lookahead_target = Vector2.ZERO
		
	var turbulence_vector := Vector2.ZERO
	if _dialetheic_turbulence > 0.001:
		turbulence_vector = Vector2(
			randf_range(-1.0, 1.0),
			randf_range(-1.0, 1.0)
		) * _dialetheic_turbulence * 4.0
		_dialetheic_turbulence = move_toward(_dialetheic_turbulence, 0.0, delta * 3.5)
		
	var desired_camera_pos := global_position + lookahead_target + turbulence_vector
	target_camera.global_position = target_camera.global_position.lerp(
		desired_camera_pos,
		delta * camera_smoothing_speed
	)

# ------------------------------------------------------------------------------
# 2. State Validator (Conceived Space - Belnap-Dunn Logic & Lex I)
# ------------------------------------------------------------------------------
func _evaluate_spatial_truth(grid_coord: Vector2i) -> BelnapDunnValue:
	if not _spatial_truth_matrix.has(grid_coord):
		return BelnapDunnValue.N
	return _spatial_truth_matrix[grid_coord]

func set_coordinate_truth(grid_coord: Vector2i, truth_val: BelnapDunnValue) -> void:
	var old_val: BelnapDunnValue = _spatial_truth_matrix.get(grid_coord, BelnapDunnValue.N)
	_spatial_truth_matrix[grid_coord] = truth_val
	
	_commit_telemetry_event("COORDINATE_STATE_MUTATION", {
		"grid_coordinate": [grid_coord.x, grid_coord.y],
		"previous_state": old_val,
		"new_state": truth_val,
		"ego_density": ego_density
	})

func _resolve_dialetheic_step(grid_coord: Vector2i, incoming_velocity: Vector2, _delta: float) -> Vector2:
	dialetheic_collision_detected.emit(Vector2(grid_coord.x * 16.0, grid_coord.y * 16.0), "METAMORPHIC_SQUEEZE")
	set_liturgical_animation(&"dialetheic_shift", 0.8)
	
	if not enable_metamorphic_squeeze:
		return Vector2.ZERO
		
	var algorithmic_cost: float = 0.28
	var scar_data := {
		"coordinate": [grid_coord.x, grid_coord.y],
		"timestamp_usec": Time.get_ticks_usec(),
		"algorithmic_cost": algorithmic_cost,
		"spectral_signature": active_spectral_constant,
		"ego_density_at_formation": ego_density,
		"structural_load_capacity": 1.0 / algorithmic_cost
	}
	
	_harmonic_scars.append(scar_data)
	_spatial_truth_matrix[grid_coord] = BelnapDunnValue.T
	_dialetheic_turbulence = 1.0
	
	harmonic_scar_petrified.emit(scar_data)
	_commit_telemetry_event("HARMONIC_SCAR_PETRIFIED", scar_data)
	
	return incoming_velocity * 0.82

func _crystallize_unindexed_coordinate(grid_coord: Vector2i) -> void:
	_spatial_truth_matrix[grid_coord] = BelnapDunnValue.F
	_commit_telemetry_event("AXIOMATIC_ECHOLOCATION_CRYSTALLIZE", {
		"grid_coordinate": [grid_coord.x, grid_coord.y],
		"crystallized_as": "GLASS_LOGIC_BLOCKED"
	})

# ------------------------------------------------------------------------------
# 3. Ash Archive (Lex I: Never-Overwrite Append-Only Merkle DAG Ledger)
# ------------------------------------------------------------------------------
func _initialize_ash_archive() -> void:
	_ash_archive_ledger.clear()
	_latest_block_hash = GENESIS_HASH

func _commit_telemetry_event(event_type: String, payload: Dictionary) -> Dictionary:
	var event_index: int = _ash_archive_ledger.size()
	var timestamp: int = Time.get_ticks_usec()
	
	var raw_serialized := "%d|%d|%s|%s|%s" % [
		event_index,
		timestamp,
		_latest_block_hash,
		event_type,
		JSON.stringify(payload)
	]
	
	var event_hash := raw_serialized.sha256_text()
	
	var event_record := {
		"index": event_index,
		"timestamp_usec": timestamp,
		"prev_hash": _latest_block_hash,
		"hash": event_hash,
		"event_type": event_type,
		"payload": payload
	}
	
	_ash_archive_ledger.append(event_record)
	_latest_block_hash = event_hash
	
	state_transition_committed.emit(event_record)
	return event_record

func get_ash_archive_ledger_count() -> int:
	return _ash_archive_ledger.size()

func verify_ash_archive_integrity() -> bool:
	var current_hash := GENESIS_HASH
	for i in range(_ash_archive_ledger.size()):
		var record: Dictionary = _ash_archive_ledger[i]
		if record["prev_hash"] != current_hash:
			push_error("Ash Archive Integrity Fault at index %d: Parent hash mismatch." % i)
			return false
			
		var recomputed_serialized := "%d|%d|%s|%s|%s" % [
			record["index"],
			record["timestamp_usec"],
			record["prev_hash"],
			record["event_type"],
			JSON.stringify(record["payload"])
		]
		
		if recomputed_serialized.sha256_text() != record["hash"]:
			push_error("Ash Archive Integrity Fault at index %d: Payload tampering detected." % i)
			return false
			
		current_hash = record["hash"]
	return true

# ------------------------------------------------------------------------------
# 4. Lived Space & Bio-Semantic Visual Pipeline
# ------------------------------------------------------------------------------
func _calculate_afield_kinetics() -> void:
	var density_ratio: float = ego_density / BASELINE_EGO_DENSITY
	_current_afield_radius = BASELINE_AFIELD_RADIUS * (1.0 + (afield_beta * _current_emotional_magnitude * density_ratio))

func _update_lived_space_visuals() -> void:
	if not animated_sprite or not animated_sprite.material:
		return
		
	var mat := animated_sprite.material as ShaderMaterial
	if not mat:
		return
		
	var cadence_gain: float = 1.0 + (dialogue_cadence_intensity * 0.45)
	mat.set_shader_parameter("u_afield_potency", _current_afield_radius / BASELINE_AFIELD_RADIUS)
	mat.set_shader_parameter("u_lumen_emission_gain", cadence_gain)
	mat.set_shader_parameter("u_active_spectral_constant", int(active_spectral_constant))
	
	lumen_cadence_pulsed.emit(cadence_gain, int(active_spectral_constant))

func pulse_dialogue_stress(stress_syllable: float) -> void:
	dialogue_cadence_intensity = stress_syllable
	set_liturgical_animation(&"penitent_recitation", 0.6)
	
	_commit_telemetry_event("DIALOGUE_CADENCE_PULSE", {
		"syllable_stress": stress_syllable,
		"resulting_gain": 1.0 + (stress_syllable * 0.45),
		"spectral_constant": active_spectral_constant
	})
