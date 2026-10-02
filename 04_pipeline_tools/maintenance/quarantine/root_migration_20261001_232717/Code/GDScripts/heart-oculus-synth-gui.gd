# =============================================================================
#          NYX AURELIA: SPATIAL AUDIO SYNTHESIS TERMINAL CONTROLLER
#                   SCRIPT: heart-oculus-synth-gui.gd
# =============================================================================
# Direct interactive interface for HeartOculusSynth and HeartOculusReactor.
# Allows manual manipulation of volume layers, detuning widths, and dialetheic
# friction vectors to audibly demonstrate paraconsistent phase beating.
# =============================================================================

extends Control
class_name HeartOculusSynthGUI

# --- UI Node References (Assign in Inspector or auto-resolved in _ready)
@export_group("Sliders")
@export var primary_vol_slider: HSlider
@export var sub_vol_slider: HSlider
@export var detune_width_slider: HSlider
@export var dialetheism_slider: HSlider # Manually drive the D-index to hear beating
@export var sweep_duration_slider: HSlider

@export_group("Status Labels")
@export var status_text: Label
@export var primary_freq_text: Label
@export var sub_freq_text: Label
@export var beating_rate_text: Label

@export_group("Buttons & Toggles")
@export var trigger_sweep_btn: Button
@export var loop_sub_toggle: CheckButton

# --- Target Node Paths
@export_group("Target Nodes")
## The active synthesizer node. If null, will look for a child or sibling node.
@export var synth_node: HeartOculusSynth

# --- Internal Variables
var _synth: HeartOculusSynth

func _ready() -> void:
	# 1. Resolve synth node reference
	if synth_node:
		_synth = synth_node
	elif has_node("HeartOculusSynth"):
		_synth = get_node("HeartOculusSynth") as HeartOculusSynth
	elif get_parent().has_node("HeartOculusSynth"):
		_synth = get_parent().get_node("HeartOculusSynth") as HeartOculusSynth
	
	if not _synth:
		push_error("[Synth GUI] Initialization failed: 'HeartOculusSynth' node not found.")
		if status_text:
			status_text.text = "SYNTHESIS OFFLINE: NODE NOT FOUND"
			status_text.add_theme_color_override("font_color", Color(0.9, 0.22, 0.22))
		return

	# 2. Bind Signals from Controls to Synth Variables
	_bind_ui_signals()
	
	# 3. Synchronize Initial UI States with Synth Defaults
	_sync_ui_to_synth()
	
	if status_text:
		status_text.text = "SYNTHESIS INTERFACE ACTIVE // SPECTRAL: BLUE/SORROW"
		status_text.add_theme_color_override("font_color", Color(0.60, 0.36, 0.82)) # Vibrant Violet

func _process(_delta: float) -> void:
	if not _synth or not _synth._is_active:
		# If the manual Dialetheism slider is being held, we update frequency readouts in real-time
		if dialetheism_slider and not _synth._is_active:
			_update_telemetry_labels(
				_synth.f_start * pow(_synth.f_end / _synth.f_start, 0.0), # Static starting freq or current
				dialetheism_slider.value / 100.0
			)
		return
		
	# Synchronize active sweep values to labels
	_update_telemetry_labels(_synth._playback if _synth else 0.0, _synth.get_parent().get_dialetheism_index() if _synth.get_parent() and _synth.get_parent().has_method("get_dialetheism_index") else dialetheism_slider.value / 100.0)

# --- Signal Interfacing & Binding
func _bind_ui_signals() -> void:
	if primary_vol_slider:
		primary_vol_slider.value_changed.connect(_on_primary_vol_changed)
	if sub_vol_slider:
		sub_vol_slider.value_changed.connect(_on_sub_vol_changed)
	if detune_width_slider:
		detune_width_slider.value_changed.connect(_on_detune_width_changed)
	if dialetheism_slider:
		dialetheism_slider.value_changed.connect(_on_dialetheism_changed)
	if sweep_duration_slider:
		sweep_duration_slider.value_changed.connect(_on_sweep_duration_changed)
	if trigger_sweep_btn:
		trigger_sweep_btn.pressed.connect(_on_trigger_sweep_pressed)
	if loop_sub_toggle:
		loop_sub_toggle.toggled.connect(_on_loop_sub_toggled)

func _sync_ui_to_synth() -> void:
	# Convert synth volume/decibel structures back to percentages [0, 100]
	if primary_vol_slider:
		primary_vol_slider.value = 80.0 # Default starting primary volume percentage
	if sub_vol_slider:
		sub_vol_slider.value = 50.0 # Default starting sub-bass percentage
	if detune_width_slider:
		detune_width_slider.value = _synth.max_detune_width * 1000.0 # Map 0.015 to 15.0
	if dialetheism_slider:
		dialetheism_slider.value = 0.0
	if sweep_duration_slider:
		sweep_duration_slider.value = _synth.duration
	if loop_sub_toggle:
		loop_sub_toggle.button_pressed = false

# --- Callback Actions
func _on_primary_vol_changed(value: float) -> void:
	# Convert flat slider percentage to scalar volume dampening
	_synth.volume_db = linear_to_db(value / 100.0)

func _on_sub_vol_changed(value: float) -> void:
	# Directly modulate the baseline mix level of the detuned sub-bass voice
	# This dictates how prominently the phase beating is physically heard
	if "sub_bass_multiplier" in _synth:
		_synth.sub_bass_multiplier = value / 100.0

func _on_detune_width_changed(value: float) -> void:
	# Modify the detuning limit (maps 0-50 slider back to 0.0 - 0.05 scaling factor)
	_synth.max_detune_width = value / 1000.0

func _on_dialetheism_changed(value: float) -> void:
	var d_factor: float = value / 100.0
	
	# Drive the manual A-Field integration directly if the simulation is not actively sweeping
	if not _synth._is_active:
		if get_node_or_null("/root/HeartOculusReactor"):
			var reactor = get_node("/root/HeartOculusReactor")
			# Adjust reactor metrics dynamically based on manual slider
			reactor.t = 1.0
			reactor.f = d_factor
			reactor._evaluate_system_state()
			reactor._emit_state_update()
		else:
			# Fallback if standalone: force detuning directly on the synthesizer
			_synth.trigger_standalone_modulation(d_factor)
			
	_update_telemetry_labels(
		_synth.f_start, 
		d_factor
	)

func _on_sweep_duration_changed(value: float) -> void:
	_synth.duration = value

func _on_trigger_sweep_pressed() -> void:
	if _synth:
		# Reset manual Dialetheism slider back to zero during active sweep
		if dialetheism_slider:
			dialetheism_slider.value = 0.0
			
		# If linked to the main reactor autoload, let it run the full structural collapse sequence
		if get_node_or_null("/root/HeartOculusReactor"):
			var reactor = get_node("/root/HeartOculusReactor")
			reactor.trigger_sector_four_collapse()
		else:
			# Standalone fallback sweep execution
			_synth.trigger_acoustic_glide()
			
		if status_text:
			status_text.text = "ACTIVE COLLAPSE GLIDE SIMULATION IN PROGRESS..."
			status_text.add_theme_color_override("font_color", Color(0.95, 0.76, 0.20)) # Amber Yellow

func _on_loop_sub_toggled(button_pressed: bool) -> void:
	# Forces the synthesizer to loop the sub-bass at a constant static pitch (A1)
	# allowing players to focus entirely on listening to the physical detuning wave offsets
	if "force_sub_bass_loop" in _synth:
		_synth.force_sub_bass_loop = button_pressed
		if status_text:
			if button_pressed:
				status_text.text = "SUB-BASS LOOP ACTIVATED: MANUAL BEATING DEMONSTRATION"
				status_text.add_theme_color_override("font_color", Color(0.46, 0.82, 0.35)) # Green
			else:
				status_text.text = "SYNTHESIS INTERFACE ACTIVE // SPECTRAL: BLUE/SORROW"
				status_text.add_theme_color_override("font_color", Color(0.60, 0.36, 0.82))

# --- UI Telemetry Readouts
func _update_telemetry_labels(active_hz: float, active_d: float) -> void:
	# Resolve the actual current running primary frequency
	var current_primary: float = active_hz
	if _synth._is_active:
		var t_ratio = _synth._time_elapsed / _synth.duration
		current_primary = _synth.f_start * pow(_synth.f_end / _synth.f_start, t_ratio)
	
	# If force loop is active, the primary anchor for sub-bass is hard-clamped to A1 (55Hz)
	var sub_anchor: float = current_primary * 0.5
	if _synth.get("force_sub_bass_loop") == true:
		sub_anchor = _synth.f_end
		
	var sub_voice_1: float = sub_anchor
	var sub_voice_2: float = sub_anchor * (1.0 + active_d * _synth.max_detune_width)
	
	# Beating rate is the absolute physical frequency difference between the two detuned sub-voices
	# beat_frequency = |f1 - f2|
	var beat_hz: float = abs(sub_voice_1 - sub_voice_2) if active_d > 0.0 else 0.0

	if primary_freq_text:
		primary_freq_text.text = "Primary Glide: %.2f Hz" % current_primary
	if sub_freq_text:
		sub_freq_text.text = "Sub-Voices: Voice A: %.2f Hz | Voice B: %.2f Hz" % [sub_voice_1, sub_voice_2]
	if beating_rate_text:
		if beat_hz > 0.0:
			beating_rate_text.text = "A-Field Interference: %.3f Hz (Beats per second)" % beat_hz
		else:
			beating_rate_text.text = "A-Field Interference: Phase Aligned (0.000 Hz)"
