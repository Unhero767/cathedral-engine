class_name CathedralAvatarPortrait
extends AnimatedSprite2D

## EAS-03 Cathedral-Born Avatar Portrait Controller
## Manages 6 Liturgical Animation cycles, CanvasItem shader parameters,
## phoneme stress dynamic pulsing, and Layer 11 runtime scar injections.

signal liturgical_state_changed(previous_state: StringName, new_state: StringName)
signal lumen_pulse_peaked(gain: float)

@export_group("Liturgy & Archetype")
@export var character_recipe_path: String = ""
@export var default_liturgy: StringName = &"liturgical_idle"
@export var base_afield_potency: float = 0.87

@export_group("Dialogue Cadence")
@export var speech_gain_multiplier: float = 0.45
@export var recovery_rate: float = 4.0

var _current_lumen_gain: float = 1.0
var _target_lumen_gain: float = 1.0
var _portrait_material: ShaderMaterial

func _ready() -> void:
	_portrait_material = material as ShaderMaterial
	if _portrait_material != null:
		_portrait_material.set_shader_parameter("u_afield_potency", base_afield_potency)
	
	if sprite_frames != null and sprite_frames.has_animation(default_liturgy):
		play(default_liturgy)
	
	print("[CathedralAvatarPortrait] Ready. Press 1-6 for Liturgical States, Spacebar for Dialogue Stress Pulse.")

func _process(delta: float) -> void:
	if not is_equal_approx(_current_lumen_gain, _target_lumen_gain):
		_current_lumen_gain = move_toward(_current_lumen_gain, _target_lumen_gain, recovery_rate * delta)
		if _portrait_material != null:
			_portrait_material.set_shader_parameter("u_lumen_emission_gain", _current_lumen_gain)

## Intercepts dialogue phoneme stress and drives physical luminosity
func pulse_dialogue_stress(syllable_stress: float, trigger_recitation: bool = true) -> void:
	_target_lumen_gain = 1.0 + (clampf(syllable_stress, 0.0, 1.0) * speech_gain_multiplier)
	if trigger_recitation and sprite_frames != null and sprite_frames.has_animation(&"penitent_recitation"):
		play(&"penitent_recitation")

func return_to_idle() -> void:
	_target_lumen_gain = 1.0
	if sprite_frames != null and sprite_frames.has_animation(default_liturgy):
		play(default_liturgy)

func set_liturgical_state(new_state: StringName) -> void:
	if sprite_frames != null and sprite_frames.has_animation(new_state):
		var prev := animation
		play(new_state)
		print("[Liturgy State] Switched: ", prev, " -> ", new_state)
		liturgical_state_changed.emit(prev, new_state)

## Live Interactive Test Harness
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.is_pressed() and not event.is_echo():
		match event.keycode:
			KEY_1:
				set_liturgical_state(&"liturgical_idle")
			KEY_2:
				set_liturgical_state(&"lumen_pulse")
			KEY_3:
				set_liturgical_state(&"ocular_surge")
			KEY_4:
				set_liturgical_state(&"harmonic_resonance")
			KEY_5:
				set_liturgical_state(&"dialetheic_shift")
			KEY_6:
				set_liturgical_state(&"penitent_recitation")
			KEY_SPACE:
				print("[Dialogue Physics] High-stress phoneme pulse triggered (Gain: ", 1.0 + speech_gain_multiplier, ")")
				pulse_dialogue_stress(1.0, true)
			KEY_ESCAPE:
				return_to_idle()
