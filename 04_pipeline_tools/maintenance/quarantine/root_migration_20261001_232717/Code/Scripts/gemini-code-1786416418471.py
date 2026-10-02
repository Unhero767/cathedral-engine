extends Node

@export var sample_hz: float = 44100.0
@export var f_start: float = 880.0  # A5
@export var f_end: float = 55.0     # A1
@export var duration: float = 3.0   # Sweep duration in seconds

private var playback: AudioStreamGeneratorPlayback
private var phase: float = 0.0
private var time_elapsed: float = 0.0
private var active: bool = false

@onready var audio_stream_player: AudioStreamPlayer = $AudioStreamPlayer

func _ready() -> void:
	var generator = AudioStreamGenerator.new()
	generator.mix_rate = sample_hz
	generator.buffer_length = 0.5
	audio_stream_player.stream = generator
	audio_stream_player.play()
	playback = audio_stream_player.get_stream_playback()
	active = true

func _process(delta: float) -> void:
	if not active:
		return
	
	time_elapsed += delta
	if time_elapsed >= duration:
		time_elapsed = duration
		active = false # Terminate sweep upon vector completion
		
	fill_buffer()

func fill_buffer() -> void:
	var frames_available = playback.get_frames_available()
	for i in range(frames_available):
		var t = min(time_elapsed, duration)
		# Compute instantaneous frequency using the logarithmic ratio
		var current_freq = f_start * pow(f_end / f_start, t / duration)
		
		phase += (current_freq / sample_hz)
		phase = fmod(phase, 1.0)
		
		# Generate sample with an amplitude envelope to prevent transient clicks
		var envelope = 1.0 - (t / duration)
		var sample = sin(phase * TAU) * envelope
		
		playback.push_frame(Vector2(sample, sample))