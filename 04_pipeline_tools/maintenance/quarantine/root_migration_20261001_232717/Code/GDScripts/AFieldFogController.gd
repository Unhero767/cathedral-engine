# =============================================================================
#          NYX AURELIA: 3D VOLUMETRIC FOG CONTROLLER
#                 SCRIPT: AFieldFogController.gd
# =============================================================================
# Controls global WorldEnvironment volumetric fog and localized boundary 
# FogVolume nodes, dynamically sweeping purple/violet mist inward as A-Field 
# stability degrades under paraconsistent or underdetermined state transitions.
# Governed by the core axiom: Emotion = Physics = Magic = Biology = Architecture.
# =============================================================================

extends Node3D
class_name AFieldFogController

# --- Node References (Assign in the Inspector)
@export_group("Target Nodes")
## Optional: Reference to the global WorldEnvironment node to drive global volumetric fog.
@export var world_environment: WorldEnvironment
## Optional: Array of FogVolume nodes representing the boundaries/perimeter of the combat arena.
@export var boundary_fog_volumes: Array[FogVolume] = []
## Optional: The central node (or player) towards which boundary fog volumes sweep inward. Defaults to parent.
@export var sweep_target: Node3D

# --- Tuning Parameters
@export_group("Global Volumetric Fog Tuning")
## Fog density when the A-Field is pristine and stable.
@export var stable_density: float = 0.005
## Max fog density when physical reality has completely dissolved.
@export var max_dissolution_density: float = 0.25
## Baseline color of the environment under stable, classical conditions.
@export var stable_color: Color = Color(0.04, 0.04, 0.06, 1.0) # Cold industrial slate-gray
## Color of the mist during active dialetheic stabilization (Harmonic Scar).
@export var harmonic_scar_color: Color = Color(0.60, 0.36, 0.82, 1.0) # Signature Violet (#995CD1)
## Color of the mist under total dissolution (Critical System Exhaustion).
@export var dissolution_color: Color = Color(0.12, 0.08, 0.18, 1.0) # Obsidian Violet (#1F142D)

@export_group("Boundary Sweep Tuning")
## Speed of the lerp interpolation for fog densities and spatial transitions.
@export var sweep_interpolation_speed: float = 1.5
## Maximum percentage distance the boundary FogVolumes can sweep inward toward the target center (0.0 to 0.85).
@export var max_sweep_inward_pct: float = 0.65
## Scaling multiplier applied to the boundary FogVolume sizes as they sweep inward.
@export var boundary_size_expansion: float = 1.5

# --- Internal Telemetry Tracking
var _target_density: float = 0.005
var _target_color: Color = Color(0.04, 0.04, 0.06, 1.0)
var _target_emission_color: Color = Color.BLACK
var _boundary_sweep_factor: float = 0.0 ## Target sweep factor (0.0 = pushed to bounds, 1.0 = fully swept inward)
var _current_sweep_value: float = 0.0 ## Smoothed, active sweep factor interpolating over frames

# Cache original boundary transforms to allow robust, non-cumulative sweeping
var _original_positions: Array[Vector3] = []
var _original_sizes: Array[Vector3] = []

# =============================================================================
# Built-In Virtual Methods
# =============================================================================

func _ready() -> void:
	# Default sweep target to parent node if not explicitly assigned
	if not sweep_target and get_parent() is Node3D:
		sweep_target = get_parent() as Node3D
		
	# Cache original transforms of boundary volumes to allow exact offset math
	_original_positions.resize(boundary_fog_volumes.size())
	_original_sizes.resize(boundary_fog_volumes.size())
	for i in range(boundary_fog_volumes.size()):
		var fog_vol = boundary_fog_volumes[i]
		if fog_vol:
			_original_positions[i] = fog_vol.global_position
			_original_sizes[i] = fog_vol.size
			
	# Connect dynamically to the HeartOculusReactor autoload singleton
	if _is_autoload_present("HeartOculusReactor"):
		var reactor = get_node("/root/HeartOculusReactor")
		reactor.state_changed.connect(_on_reactor_state_changed)
		reactor.system_state_updated.connect(_on_reactor_system_state_updated)
		push_log("Successfully interlinked A-Field Volumetric Fog with telemetry stream.")
	else:
		push_warning("Autoload 'HeartOculusReactor' not found. Volumetric fog controller operating in manual mode.")


func _process(delta: float) -> void:
	# 1. Smoothly interpolate global WorldEnvironment volumetric fog
	if world_environment and world_environment.environment:
		var env = world_environment.environment
		if env.volumetric_fog_enabled:
			# Interpolate density
			env.volumetric_fog_density = lerp(
				env.volumetric_fog_density, 
				_target_density, 
				delta * sweep_interpolation_speed
			)
			# Interpolate albedo color
			env.volumetric_fog_albedo = env.volumetric_fog_albedo.lerp(
				_target_color, 
				delta * sweep_interpolation_speed
			)
			# Interpolate emission (glowing fog effect during active resonance)
			env.volumetric_fog_emission = env.volumetric_fog_emission.lerp(
				_target_emission_color, 
				delta * sweep_interpolation_speed
			)
			
	# 2. Smoothly sweep boundary FogVolumes inward toward target center
	if boundary_fog_volumes.size() > 0 and sweep_target:
		# Smoothly slide the active sweep factor toward target telemetry
		_current_sweep_value = lerp(
			_current_sweep_value, 
			_boundary_sweep_factor, 
			delta * sweep_interpolation_speed
		)
		
		var center_pos = sweep_target.global_position
		
		for i in range(boundary_fog_volumes.size()):
			var fog_vol = boundary_fog_volumes[i]
			if not fog_vol: continue
			
			var orig_pos = _original_positions[i]
			var orig_size = _original_sizes[i]
			
			# Calculate vector from boundary position to central target
			var to_center = center_pos - orig_pos
			
			# Sweep position inward based on sweep percentage
			var target_pos = orig_pos + (to_center * _current_sweep_value * max_sweep_inward_pct)
			fog_vol.global_position = fog_vol.global_position.lerp(
				target_pos, 
				delta * sweep_interpolation_speed
			)
			
			# Expand scale to prevent gaps between volumes as they converge
			var target_size = orig_size * (1.0 + (_current_sweep_value * (boundary_size_expansion - 1.0)))
			fog_vol.size = fog_vol.size.lerp(target_size, delta * sweep_interpolation_speed)
			
			# Drive local FogMaterial parameters if a material is active
			if fog_vol.material is FogMaterial:
				var mat = fog_vol.material as FogMaterial
				# Local albedo tracks global target color
				mat.albedo = mat.albedo.lerp(_target_color, delta * sweep_interpolation_speed)
				# local density scales with the sweep intensity
				var local_target_density = lerp(0.01, 2.0, _current_sweep_value)
				mat.density = lerp(mat.density, local_target_density, delta * sweep_interpolation_speed)
				# Emissive glow on the boundary fog during active buffer
				mat.emission = mat.emission.lerp(_target_emission_color * 1.5, delta * sweep_interpolation_speed)


# =============================================================================
# Telemetry Signal Listeners
# =============================================================================

## Driven by continuous state shifts. Tracks Dialetheism (D) and Underdetermination (U).
func _on_reactor_state_changed(t: float, f: float, dialetheism: float, underdetermination: float) -> void:
	# Underdetermination (U) represents spatial dissolution. It directly scales global density.
	_target_density = lerp(stable_density, max_dissolution_density, underdetermination)
	
	# The boundary sweep is driven by a combination of active paraconsistent tension (D) and dissolution (U).
	# As either metric spikes, the boundary volumes physically encroach on the arena center.
	_boundary_sweep_factor = clamp(dialetheism + underdetermination, 0.0, 1.0)


## Driven by system classification states. Shift albedo and emission spectral signatures.
func _on_reactor_system_state_updated(state_name: String, state_color: Color) -> void:
	match state_name:
		"CLASSICAL NOMINAL":
			_target_color = stable_color
			_target_emission_color = Color.BLACK # No active glow
			
		"TRANSITIONAL MATRIX":
			# Interpolate to a destabilizing amber-violet hybrid
			_target_color = stable_color.lerp(harmonic_scar_color, 0.4)
			_target_emission_color = harmonic_scar_color * 0.1
			
		"HARMONIC SCAR (STABILIZED)":
			# Deep glowing violet representing stabilized persistent contradiction
			_target_color = harmonic_scar_color
			# Apply active HDR emissive glow to the volumetric fog
			_target_emission_color = harmonic_scar_color * 0.45
			
		"CRITICAL SYSTEM EXHAUSTION":
			# Dense, light-absorbing obsidian-violet void
			_target_color = dissolution_color
			_target_emission_color = dissolution_color * 0.12


# =============================================================================
# Helper Utilities
# =============================================================================

func _is_autoload_present(node_name: String) -> bool:
	return get_tree().root.has_node(node_name)


func push_log(msg: String) -> void:
	print("[AFieldFogController] %s" % msg)
