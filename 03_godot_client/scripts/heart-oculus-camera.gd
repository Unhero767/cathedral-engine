#==============================================================================
# heart-oculus-camera.gd
#==============================================================================
# ORGANIC COGNITIVE CAMERA SHAKE CONTROLLER (Godot 4.x / GDScript 2.0)
# Designed as an extension of Camera2D.
# Interlinks with the HeartOculusReactor Autoload Singleton.
# Implements FastNoiseLite-driven non-linear screenshake.
#==============================================================================

extends Camera2D
class_name HeartOculusCamera

#--- Noise Parameters for Organic Motion
@export_group("Noise Profiling")
## Noise generator for organic, non-repetitive shake patterns.
@export var noise: FastNoiseLite = FastNoiseLite.new()
## Base frequency of the shake oscillation. Higher = faster trembling.
@export var shake_speed: float = 30.0

#--- Shake Limits
@export_group("Shake Offsets")
## Maximum translation offset in pixels along the X and Y axes.
@export var max_offset: Vector2 = Vector2(100.0, 75.0)
## Maximum rotational roll in degrees (automatically converted to radians).
@export var max_roll: float = 0.15 # Approx 8.5 degrees

#--- Decay Tuning
@export_group("Mathematical Decay")
## The exponent of the decay curve. 1.0 is linear, 2.0 is quadratic, 3.0 is cubic.
## Higher values cause the shake to drop off rapidly at first, then settle gently.
@export var shake_power: float = 2.0
## Recovery speed. How fast the shake trauma decays back to 0.0 per second.
@export var decay_rate: float = 1.2

#--- Real-Time Tracking
var _trauma: float = 0.0 ## Current shake intensity [0.0, 1.0]
var _time_elapsed: float = 0.0

#==============================================================================
# Built-In Virtual Methods
#==============================================================================

func _ready() -> void:
	randomize()
	_initialize_noise_profile()
	
	# Connect dynamically to the HeartOculusReactor singleton signals
	if _is_autoload_present("HeartOculusReactor"):
		var reactor = get_node("/root/HeartOculusReactor")
		reactor.critical_anomaly_triggered.connect(_on_reactor_critical_anomaly_triggered)
		reactor.harmonic_scar_stabilized.connect(_on_reactor_harmonic_scar_stabilized)
		reactor.state_changed.connect(_on_reactor_state_changed)
		push_log("Interlinked with HeartOculusReactor camera telemetry.")
	else:
		push_warning("Camera Node: 'HeartOculusReactor' Autoload not found. Signal shake disabled.")


func _process(delta: float) -> void:
	if _trauma > 0.0:
		_time_elapsed += delta * shake_speed
		
		# Decay the trauma level smoothly over time
		_trauma = max(_trauma - decay_rate * delta, 0.0)
		
		# Apply non-linear decay to trauma to calculate final visual strength
		# strength = trauma ^ shake_power
		var strength: float = pow(_trauma, shake_power)
		
		# Generate multi-dimensional, organic offsets using simplex noise
		rotation = max_roll * strength * _get_noise_val(1000)
		offset.x = max_offset.x * strength * _get_noise_val(2000)
		offset.y = max_offset.y * strength * _get_noise_val(3000)
	else:
		# Return precisely to center/baseline when shake concludes
		rotation = 0.0
		offset = Vector2.ZERO


#==============================================================================
# Signal Listeners (Reactor Core Linkage)
#==============================================================================

## Severe physical collapses and explosions trigger massive, long-lasting trauma
func _on_reactor_critical_anomaly_triggered(_description: String) -> void:
	# Instantly saturate camera trauma to 100%
	add_trauma(1.0)


## Harmonic stabilization events trigger a soft, structured, resonant vibration
func _on_reactor_harmonic_scar_stabilized() -> void:
	# Add a moderate rumble that decays smoothly
	add_trauma(0.6)


## Background trembling is driven dynamically by the level of logical contradiction (Dialetheism)
func _on_reactor_state_changed(_t: float, _f: float, dialetheism: float, _underdetermination: float) -> void:
	# If there is persistent dialetheic friction, maintain a subtle baseline trembling
	if dialetheism > 0.1:
		var baseline_tremble: float = dialetheism * 0.15
		_trauma = max(_trauma, baseline_tremble)


#==============================================================================
# Public Interface & Helpers
#==============================================================================

## Public API to manually feed shock/trauma into the camera rig from general combat nodes
func add_trauma(amount: float) -> void:
	_trauma = clamp(_trauma + amount, 0.0, 1.0)


func _initialize_noise_profile() -> void:
	# Configure default simplex noise parameters if not customized in inspector
	if noise:
		noise.seed = randi()
		noise.noise_type = FastNoiseLite.TYPE_SIMPLEX
		noise.fractal_type = FastNoiseLite.FRACTAL_NONE
		noise.frequency = 0.5


func _get_noise_val(offset_seed: int) -> float:
	# Sample noise at a unique coordinate offset to prevent X and Y from oscillating identically
	return noise.get_noise_1d(_time_elapsed + offset_seed)


func _is_autoload_present(node_name: String) -> bool:
	return get_tree().root.has_node(node_name)


func push_log(msg: String) -> void:
	print("[HeartOculusCamera] %s" % msg)
