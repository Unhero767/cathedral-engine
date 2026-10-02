# ==============================================================================
# CathedralAvatarPortrait.gd
# EAS-03 Mythotechnical Portrait Controller // MLAOS-Prime
# Governed by: Book VIII (EAS-03 Somatic Layering) & Lex I (Never-Overwrite)
# ==============================================================================
class_name CathedralAvatarPortrait
extends Node2D

signal animation_cycle_completed(state_name: String)
signal scar_injected(scar_id: String, total_scars: int)

enum LiturgicalState {
	LITURGICAL_IDLE,
	LUMEN_PULSE,
	OCULAR_SURGE,
	HARMONIC_RESONANCE,
	DIALETHEIC_SHIFT,
	PENITENT_RECITATION
}

const STATE_NAMES: Dictionary = {
	LiturgicalState.LITURGICAL_IDLE: "liturgical_idle",
	LiturgicalState.LUMEN_PULSE: "lumen_pulse",
	LiturgicalState.OCULAR_SURGE: "ocular_surge",
	LiturgicalState.HARMONIC_RESONANCE: "harmonic_resonance",
	LiturgicalState.DIALETHEIC_SHIFT: "dialetheic_shift",
	LiturgicalState.PENITENT_RECITATION: "penitent_recitation"
}

# 12-Layer Auto-Z Somatic Hierarchy
const LAYER_NAMES: Array[String] = [
	"Layer00_SkeletalFrame",
	"Layer01_MuscularSomaticMass",
	"Layer02_SubcutaneousDermis",
	"Layer03_BaseLiner",
	"Layer04_UnderTunic",
	"Layer05_FlutedGorgetCuirass",
	"Layer06_ReliquaryHarness",
	"Layer07_PenitentCowl",
	"Layer08_RosaryScabbard",
	"Layer09_FacialFeaturesStubble",
	"Layer10_GildedTrikeyHalo",
	"Layer11_CustomOverlayLayer"
]

@export var afield_potency: float = 1.0:
	set(val):
		afield_potency = clamp(val, 0.0, 2.0)
		_update_shader_uniform("u_afield_potency", afield_potency)

@export var bayer_dither_intensity: float = 0.12:
	set(val):
		bayer_dither_intensity = clamp(val, 0.0, 1.0)
		_update_shader_uniform("u_bayer_dither_intensity", bayer_dither_intensity)

var current_state: LiturgicalState = LiturgicalState.DIALETHEIC_SHIFT
var layer_nodes: Dictionary = {}
var layer_11_scars: Array[Dictionary] = []
var active_shader_material: ShaderMaterial

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
	_setup_layers()
	_setup_shader_material()
	set_liturgical_state(current_state)

func _setup_layers() -> void:
	for z_index in range(LAYER_NAMES.size()):
		var layer_name: String = LAYER_NAMES[z_index]
		var layer_node: Node2D = get_node_or_null(layer_name)
		if layer_node == null:
			layer_node = Node2D.new()
			layer_node.name = layer_name
			layer_node.z_index = z_index
			add_child(layer_node)
		layer_nodes[z_index] = layer_node

func _setup_shader_material() -> void:
	var shader: Shader = load("res://cathedral_portrait_dither.gdshader") as Shader
	if shader != null:
		active_shader_material = ShaderMaterial.new()
		active_shader_material.shader = shader
		material = active_shader_material
		_update_shader_uniform("u_afield_potency", afield_potency)
		_update_shader_uniform("u_bayer_dither_intensity", bayer_dither_intensity)
		_update_shader_uniform("u_lumen_emission_gain", 1.0)

func set_liturgical_state(new_state: LiturgicalState) -> void:
	current_state = new_state
	var state_str: String = STATE_NAMES.get(new_state, "liturgical_idle")
	if animated_sprite != null and animated_sprite.sprite_frames != null:
		if animated_sprite.sprite_frames.has_animation(state_str):
			animated_sprite.play(state_str)
	print("[CathedralAvatarPortrait] Active liturgical state: %s" % state_str)

func apply_speech_stress(syllable_stress: float) -> void:
	# Formula: Gain_speech = 1.0 + (stress_syllable * 0.45)
	var lumen_gain: float = 1.0 + (clamp(syllable_stress, 0.0, 1.0) * 0.45)
	_update_shader_uniform("u_lumen_emission_gain", lumen_gain)

func inject_harmonic_scar(scar_id: String, premise_a: String, premise_b: String, residual_tension: float) -> void:
	# Under Lex I (Never-Overwrite), scars stack additively onto Layer 11
	var scar_entry: Dictionary = {
		"scar_id": scar_id,
		"premise_a": premise_a,
		"premise_b": premise_b,
		"crystallization_angle_deg": 54.74,
		"residual_tension": residual_tension,
		"timestamp": Time.get_datetime_string_from_system(true)
	}
	layer_11_scars.append(scar_entry)
	scar_injected.emit(scar_id, layer_11_scars.size())
	print("[CathedralAvatarPortrait] Lex I Invariant: Injected %s onto Layer 11 (Total: %d)" % [
		scar_id, layer_11_scars.size()
	])

func _update_shader_uniform(param_name: String, value: Variant) -> void:
	if active_shader_material != null:
		active_shader_material.set_shader_parameter(param_name, value)
