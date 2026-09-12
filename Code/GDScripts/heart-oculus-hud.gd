#==============================================================================
# heart-oculus-hud.gd
#==============================================================================
# COMPANION HUD CONTROLLER (Godot 4.x / GDScript 2.0)
# Designed to interface with the HeartOculusReactor Autoload Singleton.
# Manages dynamic progress bar animations, state labels, and screen shaders.
#==============================================================================

extends Control
class_name HeartOculusHUD

#--- UI Node Paths (Assign these in the Godot Inspector)
@export_group("Progress Bars")
@export var assertability_bar: ProgressBar
@export var deniability_bar: ProgressBar
@export var dialetheism_bar: ProgressBar
@export var underdetermination_bar: ProgressBar

@export_group("Status Indicators")
@export var state_label: Label
@export var anomaly_log: RichTextLabel

@export_group("Visual Effects")
@export var shader_rect: ColorRect # Must have a ShaderMaterial with the shader below assigned
@export var camera_shake_node: Camera2D # Optional camera for shake effects

#--- Internal State Tracking for Tweens
var _t_tween: Tween
var _f_tween: Tween
var _d_tween: Tween
var _u_tween: Tween
var _shader_tween: Tween

#==============================================================================
# Built-In Virtual Methods
#==============================================================================

func _ready() -> void:
	# Ensure HUD elements are initialized to baseline states
	_reset_hud_elements()
	
	# Verify and connect to the Autoload Singleton signals
	if Engine.has_singleton("HeartOculusReactor") or _is_autoload_present("HeartOculusReactor"):
		var reactor = get_node("/root/HeartOculusReactor")
		reactor.state_changed.connect(_on_reactor_state_changed)
		reactor.system_state_updated.connect(_on_reactor_system_state_updated)
		reactor.critical_anomaly_triggered.connect(_on_reactor_critical_anomaly_triggered)
		reactor.harmonic_scar_stabilized.connect(_on_reactor_harmonic_scar_stabilized)
		push_log("Successfully interlinked with HeartOculusReactor telemetry stream.")
	else:
		push_error("HUD Init Failure: Autoload 'HeartOculusReactor' not found in project tree.")


#==============================================================================
# Signal Callbacks (Interfacing with Reactor Singleton)
#==============================================================================

## Emitted when numerical states change; animates progress bars smoothly
func _on_reactor_state_changed(t: float, f: float, dialetheism: float, underdetermination: float) -> void:
	_animate_bar(assertability_bar, t, _t_tween)
	_animate_bar(deniability_bar, f, _f_tween)
	_animate_bar(dialetheism_bar, dialetheism, _d_tween)
	_animate_bar(underdetermination_bar, underdetermination, _u_tween)
	
	# Update shader parameters dynamically to mirror active dialetheism (contradiction depth)
	if shader_rect and shader_rect.material is ShaderMaterial:
		var mat = shader_rect.material as ShaderMaterial
		# Interpolate the raw distortion strength based on the Dialetheism Index (D)
		mat.set_shader_parameter("distortion_strength", dialetheism * 0.15)
		mat.set_shader_parameter("vignette_depth", dialetheism * 0.4)


## Emitted when the overall system state updates; adapts color and labels
func _on_reactor_system_state_updated(state_name: String, state_color: Color) -> void:
	if state_label:
		state_label.text = "COGNITIVE STATE: %s" % state_name.to_upper()
		
		# Animate the label color to match the spectral signature of the active state
		var color_tween = create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
		color_tween.tween_property(state_label, "theme_override_colors/font_color", state_color, 0.4)


## Emitted during physical/biological structural collapse
func _on_reactor_critical_anomaly_triggered(description: String) -> void:
	_log_anomaly("[color=#E63838][CRITICAL ANOMALY][/color] %s" % description)
	_trigger_camera_shake(1.5, 12.0)
	
	# Flicker the screen shader rapidly to simulate signal degradation
	if shader_rect and shader_rect.material is ShaderMaterial:
		var mat = shader_rect.material as ShaderMaterial
		var flicker_tween = create_tween().set_loops(4)
		flicker_tween.tween_method(
			func(val: float): mat.set_shader_parameter("aberration_offset", val),
			0.0, 0.05, 0.05
		).chain().tween_method(
			func(val: float): mat.set_shader_parameter("aberration_offset", val),
			0.05, 0.0, 0.05
		)


## Emitted at the exact millisecond Nyx stabilizes the paraconsistent buffer
func _on_reactor_harmonic_scar_stabilized() -> void:
	_log_anomaly("[color=#995CD1][STABILIZED][/color] Local paraconsistent boundary established. State: HARMONIC SCAR.")
	_trigger_camera_shake(0.5, 4.0)
	_flash_violet_shader()


#==============================================================================
# UI Animation Helper Methods
#==============================================================================

## Handles frame-independent progress bar value interpolation
func _animate_bar(bar: ProgressBar, target_value: float, tween_ref: Tween) -> void:
	if not bar: return
	
	if tween_ref and tween_ref.is_running():
		tween_ref.kill()
		
	# Target value is mapped from float [0.0, 1.0] to ProgressBar percentage [0.0, 100.0]
	tween_ref = create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tween_ref.tween_property(bar, "value", target_value * 100.0, 0.3)


## Triggers a radial pulse of glowing violet light when the buffer resolves
func _flash_violet_shader() -> void:
	if not shader_rect or not shader_rect.material is ShaderMaterial: return
	
	var mat = shader_rect.material as ShaderMaterial
	
	if _shader_tween and _shader_tween.is_running():
		_shader_tween.kill()
		
	_shader_tween = create_tween().set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	# Initial spike in pulse brightness
	_shader_tween.tween_method(
		func(val: float): mat.set_shader_parameter("pulse_brightness", val),
		1.0, 3.5, 0.15
	)
	# Smooth decay back to zero-state background resonance
	_shader_tween.chain().tween_method(
		func(val: float): mat.set_shader_parameter("pulse_brightness", val),
		3.5, 1.0, 1.2
	)


## Screenshake utility for tactile kinetic feedback during events
func _trigger_camera_shake(duration: float, intensity: float) -> void:
	if not camera_shake_node: return
	
	var shake_tween = create_tween().set_loops(int(duration * 20.0))
	shake_tween.tween_method(
		func(offset: Vector2): camera_shake_node.offset = offset,
		Vector2.ZERO,
		func(): return Vector2(randf_range(-intensity, intensity), randf_range(-intensity, intensity)),
		0.05
	)
	shake_tween.chain().tween_callback(func(): camera_shake_node.offset = Vector2.ZERO)


## Appends scrolling telemetry logs to the HUD terminal panel
func _log_anomaly(text: String) -> void:
	if not anomaly_log: return
	var timestamp = Time.get_time_string_from_system()
	anomaly_log.append_text("[%s] %s\n" % [timestamp, text])


## System check to locate the Autoload path in Godot’s scene tree
func _is_autoload_present(node_name: String) -> bool:
	return get_tree().root.has_node(node_name)


func _reset_hud_elements() -> void:
	if state_label:
		state_label.text = "A-FIELD SYNCING..."
	if anomaly_log:
		anomaly_log.clear()
		anomaly_log.append_text("[SYSTEM] Initializing A-Field interface telemetry...\n")
	if shader_rect and shader_rect.material is ShaderMaterial:
		var mat = shader_rect.material as ShaderMaterial
		mat.set_shader_parameter("distortion_strength", 0.0)
		mat.set_shader_parameter("vignette_depth", 0.1)
		mat.set_shader_parameter("pulse_brightness", 1.0)
		mat.set_shader_parameter("aberration_offset", 0.0)


func push_log(msg: String) -> void:
	print("[HeartOculusHUD] %s" % msg)

#==============================================================================
# COMPANION SCREEN SHADER CODE (GLSL / Godot Shader Language)
#==============================================================================
# For full visual functionality, create a new Shader resource in Godot, 
# paste the code block below, and assign it to your ColorRect's ShaderMaterial.
#==============================================================================
"""
shader_type canvas_item;

// Control parameters manipulated dynamically by the companion GDScript
uniform float distortion_strength : hint_range(0.0, 1.0) = 0.0;
uniform float vignette_depth : hint_range(0.0, 2.0) = 0.1;
uniform float pulse_brightness : hint_range(0.1, 5.0) = 1.0;
uniform float aberration_offset : hint_range(0.0, 0.2) = 0.0;

// Hardcoded Violet Spectrum Coordinates for the paraconsistent buffer representation
const vec3 VIOLET_DOMINANT = vec3(0.6, 0.36, 0.82); 

void fragment() {
	vec2 uv = SCREEN_UV;
	
	// Apply radial coordinate shift from viewport center
	vec2 center_offset = uv - vec2(0.5);
	float radial_distance = length(center_offset);
	
	// 1. Chromatic Aberration - Split color channels based on distance from center (simulates anomalies)
	vec2 red_uv = uv + (center_offset * aberration_offset);
	vec2 blue_uv = uv - (center_offset * aberration_offset);
	
	float r_channel = texture(SCREEN_TEXTURE, red_uv).r;
	float g_channel = texture(SCREEN_TEXTURE, uv).g;
	float b_channel = texture(SCREEN_TEXTURE, blue_uv).b;
	vec3 base_color = vec3(r_channel, g_channel, b_channel);
	
	// 2. Wave Distortion - Radial ripple effect linked directly to dialetheic instability
	if (distortion_strength > 0.0) {
		float sine_wave = sin(radial_distance * 40.0 - TIME * 12.0) * distortion_strength * 0.05;
		vec2 distorted_uv = uv + (center_offset * sine_wave);
		base_color = texture(SCREEN_TEXTURE, distorted_uv).rgb;
	}
	
	// 3. Violet Vignette Overlay - Darkening/violet shift crawling in from margins
	float vignette = smoothstep(0.4, 0.8 + (1.0 - vignette_depth * 0.5), radial_distance);
	vec3 colored_vignette = mix(base_color, VIOLET_DOMINANT, vignette * 0.65);
	
	// 4. Harmonic Pulse Flash - Scaled lighting effect triggered upon stabilization
	vec3 final_output = colored_vignette * (pulse_brightness + (vignette * (pulse_brightness - 1.0) * 0.5));
	
	COLOR = vec4(final_output, 1.0);
}
"""
