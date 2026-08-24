class_name SomaticToPortraitBridge
extends Node

const SomaticEngineScript = preload("res://CathedralSomaticEngine.gd")
const PortraitControllerScript = preload("res://CathedralAvatarPortrait.gd")

signal bridge_synchronized(uniform_map: Dictionary)

@export var somatic_engine: Node
@export var portrait_controller: Node

var base_afield_potency: float = 0.87

func synchronize_bridge() -> Dictionary:
	if not somatic_engine:
		return {}
	var raw_vals: PackedFloat32Array = somatic_engine.get("raw_values")
	if raw_vals.size() < 128:
		raw_vals.resize(128)
		
	var idx_cran: int = SomaticEngineScript.ParamIdx.CRANIAL_VAULT_DEPTH
	var idx_ery: int = SomaticEngineScript.ParamIdx.DERMAL_ERYTHEMA_BASAL
	var idx_mel: int = SomaticEngineScript.ParamIdx.DERMAL_MELANIN_CONCENTRATION
	var idx_af: int = SomaticEngineScript.ParamIdx.RESONANCE_AFIELD_CONDUCTANCE
	var idx_cyan: int = SomaticEngineScript.ParamIdx.RESONANCE_OCULAR_CYAN_LUMINOSITY
	
	var cran: float = max(0.8, raw_vals[idx_cran])
	var ery: float = raw_vals[idx_ery]
	var mel: float = raw_vals[idx_mel]
	var af_cond: float = max(0.5, raw_vals[idx_af])
	var cyan: float = max(0.5, raw_vals[idx_cyan])

	var shadow_ramp: float = clampf(0.65 + (cran - 1.0) * 0.25 - (ery * 0.10), 0.30, 0.90)
	var rim_factor: float = clampf(1.35 * (1.0 + ery * 0.40) * (1.0 - mel * 0.25), 0.50, 3.00)
	var afield_potency: float = clampf(base_afield_potency * af_cond, 0.0, 2.0)
	var lumen_gain: float = clampf(cyan * 1.08, 0.0, 4.0)

	var u_map := {
		"u_shadow_depth_ramp": shadow_ramp,
		"u_specular_rim_factor": rim_factor,
		"u_afield_potency": afield_potency,
		"u_lumen_emission_gain": lumen_gain
	}
	
	if portrait_controller:
		var spr = portrait_controller.get("animated_sprite")
		if spr and spr.material:
			var mat := spr.material as ShaderMaterial
			mat.set_shader_parameter("u_shadow_depth_ramp", shadow_ramp)
			mat.set_shader_parameter("u_specular_rim_factor", rim_factor)
			mat.set_shader_parameter("u_afield_potency", afield_potency)
			mat.set_shader_parameter("u_lumen_emission_gain", lumen_gain)
			
	bridge_synchronized.emit(u_map)
	return u_map

func pulse_dialogue(stress: float) -> void:
	if portrait_controller and portrait_controller.has_method("pulse_dialogue_speech"):
		portrait_controller.pulse_dialogue_speech(stress)
