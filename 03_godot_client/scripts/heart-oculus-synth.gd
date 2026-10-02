# =============================================================================
#          NYX AURELIA: CHORDAL SPATIAL SYNTHESIZER & PHASE INTERFERER
#                   SCRIPT: heart-oculus-synth.gd (Godot 4.x)
# =============================================================================
# Synthesizes real-time dual-voice logarithmic glide sweeps via AudioStreamGenerator.
# Features a primary voice sweeping logarithmically, layered with a dual-voice
# sub-bass system that detunes dynamically based on the active Dialetheism (D)
# index to create physical, heavy phase cancellation and beating as the A-Field stabilizes.
# Governed by: f(t) = f_start * (f_end / f_start) ^ (t / T)
# =============================================================================

extends AudioStreamPlayer
class_name HeartOculusSynth

@export_group("Acoustic Calibration")
## The sampling rate of the active AudioServer.
@export var sample_hz: float = 44100.0
## Initiation frequency of the logarithmic glide sweep (e.g., A5 = 880 Hz).
@export var f_start: float = 880.0
## Termination frequency of the logarithmic sweep (e.g., A1 = 55.0 Hz).
@export var f_end: float = 55.0
## Total temporal duration of the acoustic sweep in seconds.
@export var duration: float = 3.0

@export_group("Phase Modulation Tuning")
## The maximum detuning intensity for the secondary sub-bass voice.
## Higher values create faster, more aggressive beating/phase interference.
@export var max_detuning_width: float = 0.05
## Base volume ratio of the sub-bass system.
@export var sub_bass_multiplier: float = 0.70

var _playback: AudioStreamGeneratorPlayback
var _phase_primary: float = 0.0
var _phase_sub1: float = 0.0
var _phase_sub2: float = 0.0
var _time_elapsed: float = 0.0
var _is_active: bool = false
var _reactor: Node = null

func _ready() -> void:
	# 1. Programmatically instantiate the generator stream
	var generator: AudioStreamGenerator = AudioStreamGenerator.new()
	generator.mix_rate = sample_hz
	generator.buffer_length = 0.15 # Low latency buffer envelope
	stream = generator
	
	# 2. Begin playback and capture the active ring buffer
	play()
	_playback = get_stream_playback()
	
	# 3. Interlink with the HeartOculusReactor autoload if present in scene tree
	if get_node_or_null("/root/HeartOculusReactor"):
		_reactor = get_node("/root/HeartOculusReactor")
		_reactor.critical_anomaly_triggered.connect(func(_desc): trigger_acoustic_glide())
		print("[HeartOculusSynth] Interlinked with active Reactor telemetry.")
	else:
		push_warning("[HeartOculusSynth] Autoload 'HeartOculusReactor' not found. Phase modulation baseline set to static.")

func _process(_delta: float) -> void:
	if _is_active:
		_fill_synthesis_buffer()

## Dynamic trigger to initiate the logarithmic descent from active gameplay nodes
func trigger_acoustic_glide() -> void:
	_time_elapsed = 0.0
	_phase_primary = 0.0
	_phase_sub1 = 0.0
	_phase_sub2 = 0.0
	_is_active = true
	print("[HeartOculusSynth] Logarithmic glide sweep initiated.")

func _fill_synthesis_buffer() -> void:
	if not _playback:
		return
		
	var frames_available: int = _playback.get_frames_available()
	var sample_delta: float = 1.0 / sample_hz
	
	# Retrieve real-time Dialetheism (D) index from the reactor to scale phase interference
	var dialetheism: float = 0.0
	if _reactor:
		dialetheism = _reactor.get_dialetheism_index()
	else:
		# Static fallback: simulate a rising dialetheic curve over sweep duration if reactor is missing
		dialetheism = _time_elapsed / duration
	
	for i in range(frames_available):
		# Sample-accurate temporal integration to guarantee perfectly continuous sweep curvature
		var current_t: float = min(_time_elapsed + (i * sample_delta), duration)
		
		# Compute instantaneous primary frequency using the logarithmic exponential ratio
		var current_freq: float = f_start * pow(f_end / f_start, current_t / duration)
		
		# 1. Primary Voice Synthesis
		_phase_primary += (current_freq / sample_hz)
		_phase_primary = fmod(_phase_primary, 1.0)
		var primary_sample: float = sin(_phase_primary * TAU)
		
		# 2. Dual-Voice Sub-Bass Voice 1 (Standard sub-octave, e.g., current_freq * 0.5)
		var f_sub1: float = current_freq * 0.5
		_phase_sub1 += (f_sub1 / sample_hz)
		_phase_sub1 = fmod(_phase_sub1, 1.0)
		var sub_sample1: float = sin(_phase_sub1 * TAU)
		
		# 3. Dual-Voice Sub-Bass Voice 2 (Detuned sub-octave, dynamically modulated by Dialetheism)
		# Detuning width increases as Dialetheism spikes, creating heavy phase interference/beating
		var detune_factor: float = 1.0 + (dialetheism * max_detuning_width)
		var f_sub2: float = (current_freq * 0.5) * detune_factor
		_phase_sub2 += (f_sub2 / sample_hz)
		_phase_sub2 = fmod(_phase_sub2, 1.0)
		var sub_sample2: float = sin(_phase_sub2 * TAU)
		
		# Combine the sub-bass voices. When dialetheism is 0.0, they are in phase. 
		# As D increases, they beat aggressively against each other.
		var sub_bass_signal: float = (sub_sample1 + sub_sample2) * 0.5
		
		# 4. Dynamic Mix and Gain Calibration
		# Base primary volume decays over the sweep duration.
		var primary_gain: float = 0.60 * (1.0 - current_t / duration)
		# Sub-bass swells in volume and prominence as the paraconsistent buffer stabilizes.
		var sub_gain: float = sub_bass_multiplier * dialetheism
		
		# Generate composite sample wrapped in a master decay envelope to prevent transient pops
		var master_envelope: float = 1.0 - (current_t / duration)
		var composite_sample: float = (primary_sample * primary_gain + sub_bass_signal * sub_gain) * master_envelope
		
		# Push frames to Stereo Left/Right channels
		_playback.push_frame(Vector2(composite_sample, composite_sample))
		
	# Advance global sweep timer by the exact buffer chunk duration
	_time_elapsed += frames_available * sample_delta
	
	if _time_elapsed >= duration:
		_is_active = false
		print("[HeartOculusSynth] Logarithmic glide sweep completed. Phase stabilized.")
