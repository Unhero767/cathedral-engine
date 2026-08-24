class_name CathedralAvatarDebugger
extends Control

const AtlasBuilder = preload("res://CathedralAtlasBuilder.gd")
const SomaticEngineScript = preload("res://CathedralSomaticEngine.gd")
const AshArchiveScript = preload("res://CathedralAshArchive.gd")

@export var harness: Node
@export var portrait_controller: Node
@export var somatic_engine: Node
@export var somatic_bridge: Node
@export var dialogue_driver: Node

var ash_archive
var telemetry_lbl: Label
var speech_input: LineEdit
var stress_progress: ProgressBar

func _ready() -> void:
	ash_archive = AshArchiveScript.new()
	_build_ui()
	if somatic_bridge and somatic_bridge.has_signal("bridge_synchronized"):
		somatic_bridge.connect("bridge_synchronized", Callable(self, "_on_synced"))
	if dialogue_driver and dialogue_driver.has_signal("phoneme_stressed"):
		dialogue_driver.connect("phoneme_stressed", Callable(self, "_on_phoneme_stressed"))

func _build_ui() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)

	var scroll := ScrollContainer.new()
	scroll.set_anchors_preset(Control.PRESET_FULL_RECT)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	add_child(scroll)

	var margin := MarginContainer.new()
	margin.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	margin.add_theme_constant_override("margin_left", 12)
	margin.add_theme_constant_override("margin_top", 12)
	margin.add_theme_constant_override("margin_right", 12)
	margin.add_theme_constant_override("margin_bottom", 12)
	scroll.add_child(margin)

	var vbox := VBoxContainer.new()
	vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vbox.add_theme_constant_override("separation", 10)
	margin.add_child(vbox)

	var title := Label.new()
	title.text = "EAS-03 CALIBRATION & COMBAT TELEMETRY"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.35))
	vbox.add_child(title)

	vbox.add_child(HSeparator.new())

	var anim_row := HBoxContainer.new()
	vbox.add_child(anim_row)
	var anim_lbl := Label.new()
	anim_lbl.text = "Liturgical State:"
	anim_lbl.custom_minimum_size = Vector2(140, 0)
	anim_row.add_child(anim_lbl)

	var anim_opt := OptionButton.new()
	anim_opt.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for anim in AtlasBuilder.ANIMATION_DEFINITIONS: anim_opt.add_item(str(anim))
	anim_opt.item_selected.connect(func(i: int):
		if portrait_controller and portrait_controller.has_method("set_liturgical_state"):
			portrait_controller.set_liturgical_state(StringName(anim_opt.get_item_text(i)))
	)
	anim_row.add_child(anim_opt)

	vbox.add_child(HSeparator.new())

	telemetry_lbl = Label.new()
	telemetry_lbl.text = "Clearance Offsets:\n  Cranial:  +3.75 mm\n  Thoracic: +40.31 mm\n  Pelvic:   +21.25 mm\n  Femoral:  +10.00 mm\n\nActive 2D Shader Uniforms:\n  Ramp: 0.63 | Rim: 1.49 | A-Field: 1.26 | Lumen Gain: 1.00"
	telemetry_lbl.add_theme_color_override("font_color", Color(0.85, 0.90, 0.80))
	vbox.add_child(telemetry_lbl)

	vbox.add_child(HSeparator.new())

	var dlg_header := Label.new()
	dlg_header.text = "Dialogue Cadence & Speech Physics:"
	dlg_header.add_theme_color_override("font_color", Color(1.0, 0.85, 0.35))
	vbox.add_child(dlg_header)

	speech_input = LineEdit.new()
	speech_input.text = "By the blood of the Crucible and the golden light of Theta!"
	vbox.add_child(speech_input)

	var speak_btn := Button.new()
	speak_btn.text = "Simulate Speech Vocalization"
	speak_btn.pressed.connect(func():
		if dialogue_driver and dialogue_driver.has_method("speak_text_cadence"):
			dialogue_driver.speak_text_cadence(speech_input.text)
	)
	vbox.add_child(speak_btn)

	var meter_row := HBoxContainer.new()
	vbox.add_child(meter_row)
	var meter_lbl := Label.new()
	meter_lbl.text = "Lumen Emission Gain:"
	meter_lbl.custom_minimum_size = Vector2(170, 0)
	meter_row.add_child(meter_lbl)

	stress_progress = ProgressBar.new()
	stress_progress.min_value = 1.0
	stress_progress.max_value = 2.0
	stress_progress.value = 1.0
	stress_progress.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	meter_row.add_child(stress_progress)

	vbox.add_child(HSeparator.new())

	var scar_header := Label.new()
	scar_header.text = "Layer 11 Scar Inscription (Never-Overwrite):"
	scar_header.add_theme_color_override("font_color", Color(0.95, 0.45, 0.45))
	vbox.add_child(scar_header)

	var scar_row := HBoxContainer.new()
	vbox.add_child(scar_row)

	var brand_btn := Button.new()
	brand_btn.text = "+ Prayer Brand"
	brand_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	brand_btn.pressed.connect(func(): _stamp_scar(AshArchiveScript.TraumaType.PRAYER_BRAND))
	scar_row.add_child(brand_btn)

	var cut_btn := Button.new()
	cut_btn.text = "+ Combat Cut"
	cut_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	cut_btn.pressed.connect(func(): _stamp_scar(AshArchiveScript.TraumaType.COMBAT_LACERATION))
	scar_row.add_child(cut_btn)

	var ash_btn := Button.new()
	ash_btn.text = "+ Carbon Ash"
	ash_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	ash_btn.pressed.connect(func(): _stamp_scar(AshArchiveScript.TraumaType.ASH_DEPOSIT))
	scar_row.add_child(ash_btn)

func _stamp_scar(type) -> void:
	if ash_archive and portrait_controller:
		var uv := Vector2(randf_range(0.40, 0.60), randf_range(0.35, 0.55))
		ash_archive.inscribe_trauma(type, uv, randf_range(0.70, 1.00))
		if portrait_controller.has_method("inject_custom_pixel_layer"):
			portrait_controller.inject_custom_pixel_layer(ash_archive.get_texture())

func _on_synced(u: Dictionary) -> void:
	if telemetry_lbl and somatic_engine:
		var raw_vals: PackedFloat32Array = somatic_engine.get("raw_values")
		if raw_vals.size() >= 128:
			var visc = raw_vals[SomaticEngineScript.ParamIdx.ADIPOSE_VISCERAL]
			var cran = raw_vals[SomaticEngineScript.ParamIdx.CRANIAL_VAULT_DEPTH]
			var pec = raw_vals[SomaticEngineScript.ParamIdx.HYPERTROPHY_PECTORALIS_MAJOR]
			var fem = raw_vals[SomaticEngineScript.ParamIdx.ADIPOSE_FEMORAL_ANTERIOR]
			telemetry_lbl.text = "Clearance Offsets:\n  Cranial:  %+.2f mm\n  Thoracic: %+.2f mm\n  Pelvic:   %+.2f mm\n  Femoral:  %+.2f mm\n\nActive 2D Shader Uniforms:\n  Ramp: %.2f | Rim: %.2f | A-Field: %.2f | Lumen Gain: %.2f" % [
				(cran - 1.0) * 25.0, (visc * 0.75 * 35.0) + (pec * 20.0), visc * 25.0, fem * 25.0,
				u.get("u_shadow_depth_ramp", 0.65), u.get("u_specular_rim_factor", 1.35), u.get("u_afield_potency", 0.87), u.get("u_lumen_emission_gain", 1.00)
			]

func _on_phoneme_stressed(_token: String, _stress: float, gain: float) -> void:
	if stress_progress: stress_progress.value = gain
