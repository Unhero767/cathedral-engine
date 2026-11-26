# CarrierSynthesizer.gd
# Real-Time 42.0 Hz / 1.5 Hz Binaural Carrier Wave Synthesizer
class_name CarrierSynthesizer extends Node

signal audio_buffer_filled(frames_pushed: int)
signal carrier_frequency_shifted(carrier_hz: float, binaural_diff_hz: float)

@export var carrier_freq: float = 42.0
@export var somatic_mod_freq: float = 1.5
@export var sample_rate: float = 22050.0
@export var volume_amplitude: float = 0.15

var player: AudioStreamPlayer
var generator: AudioStreamGenerator
var playback: AudioStreamGeneratorPlayback

var phase_left: float = 0.0
var phase_right: float = 0.0
var somatic_phase: float = 0.0

func _ready() -> void:
	_init_audio_pipeline()

func _init_audio_pipeline() -> void:
	player = AudioStreamPlayer.new()
	generator = AudioStreamGenerator.new()
	generator.mix_rate = sample_rate
	generator.buffer_length = 0.1
	
	player.stream = generator
	add_child(player)
	player.play()
	playback = player.get_stream_playback() as AudioStreamGeneratorPlayback

func _process(_delta: float) -> void:
	if not playback:
		return
		
	var frames_available = playback.get_frames_available()
	if frames_available <= 0:
		return
		
	var delta_left = carrier_freq / sample_rate
	var delta_right = (carrier_freq + somatic_mod_freq) / sample_rate
	var delta_somatic = somatic_mod_freq / sample_rate
	
	for i in range(frames_available):
		# Calculate binaural carrier with 1.5 Hz amplitude modulation
		var mod = (sin(somatic_phase * TAU) + 1.0) * 0.5
		var sample_l = sin(phase_left * TAU) * volume_amplitude * (0.6 + 0.4 * mod)
		var sample_r = sin(phase_right * TAU) * volume_amplitude * (0.6 + 0.4 * mod)
		
		playback.push_frame(Vector2(sample_l, sample_r))
		
		phase_left = fmod(phase_left + delta_left, 1.0)
		phase_right = fmod(phase_right + delta_right, 1.0)
		somatic_phase = fmod(somatic_phase + delta_somatic, 1.0)
		
	emit_signal("audio_buffer_filled", frames_available)

func set_frequencies(new_carrier: float, new_somatic: float) -> void:
	carrier_freq = new_carrier
	somatic_mod_freq = new_somatic
	emit_signal("carrier_frequency_shifted", carrier_freq, somatic_mod_freq)
