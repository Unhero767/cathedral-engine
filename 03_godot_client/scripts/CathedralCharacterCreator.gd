class_name CathedralCharacterCreator
extends Control

const AtlasBuilder = preload("res://03_godot_client/scripts/core/CathedralAtlasBuilder.gd")
const SomaticEngineScript = preload("res://03_godot_client/scripts/core/CathedralSomaticEngine.gd")
const AshArchiveScript = preload("res://03_godot_client/scripts/CathedralAshArchive.gd")

signal character_saved(specimen_id: String, recipe_path: String, dna_path: String)
signal character_loaded(recipe_data: Dictionary)

@export var portrait_controller: Node
@export var somatic_engine: Node
@export var somatic_bridge: Node
@export var dialogue_driver: Node

const SPECTRAL_CONSTANTS: Array[Dictionary] = [
	{"id": "JOY_GOLD_THETA", "name": "Joy (Gold Theta - Θ)", "caste": "Melee Vanguard", "base_afield": 0.87, "conductance": 1.45, "visceral_fat": 0.85, "pec_hyp": 0.90, "cranial_depth": 1.15, "erythema": 0.60},
	{"id": "VOID_OBSIDIAN_NULL", "name": "Void (Obsidian Null)", "caste": "Entropic Weaver", "base_afield": 1.25, "conductance": 0.50, "visceral_fat": 0.15, "pec_hyp": 0.20, "cranial_depth": 1.28, "erythema": 0.05},
	{"id": "SORROW_BLUE_DELTA", "name": "Sorrow (Blue Delta - Δ)", "caste": "Ascetic Anchor", "base_afield": 0.60, "conductance": 0.80, "visceral_fat": 0.70, "pec_hyp": 0.40, "cranial_depth": 0.95, "erythema": 0.30},
	{"id": "CURIOSITY_TEAL_PSI", "name": "Curiosity (Teal Psi - Ψ)", "caste": "Cognitive Vanguard", "base_afield": 1.50, "conductance": 1.70, "visceral_fat": 0.35, "pec_hyp": 0.50, "cranial_depth": 1.10, "erythema": 0.25},
	{"id": "ANGER_CRIMSON_PHI", "name": "Anger (Crimson Phi - Φ)", "caste": "Shock Vanguard", "base_afield": 1.10, "conductance": 1.20, "visceral_fat": 0.30, "pec_hyp": 1.00, "cranial_depth": 1.05, "erythema": 0.85},
	{"id": "LOVE_EMERALD_EPSILON", "name": "Love (Emerald Epsilon - E)", "caste": "Biological Grounding", "base_afield": 0.95, "conductance": 1.10, "visceral_fat": 0.50, "pec_hyp": 0.60, "cranial_depth": 1.00, "erythema": 0.40},
	{"id": "FEAR_VIOLET_OMEGA", "name": "Fear (Violet Omega - Ω)", "caste": "Monastic Penitent", "base_afield": 1.30, "conductance": 1.30, "visceral_fat": 0.40, "pec_hyp": 0.50, "cranial_depth": 1.05, "erythema": 0.40}
]

var name_input: LineEdit
var specimen_id_input: LineEdit
var spectral_opt: OptionButton
var status_lbl: Label
var slider_map: Dictionary = {}

func _ready() -> void:
	_build_creator_ui()

func _build_creator_ui() -> void:
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
	title.text = "EAS-03 SPECIMEN ARCHITECT & CHARACTER CREATOR"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", Color(1.0, 0.85, 0.35))
	vbox.add_child(title)

	vbox.add_child(HSeparator.new())

	var id_row := HBoxContainer.new()
	vbox.add_child(id_row)

	var name_lbl := Label.new()
	name_lbl.text = "Specimen Name:"
	name_lbl.custom_minimum_size = Vector2(120, 0)
	id_row.add_child(name_lbl)

	name_input = LineEdit.new()
	name_input.text = "Vanguard Initiate"
	name_input.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	id_row.add_child(name_input)

	var spec_lbl := Label.new()
	spec_lbl.text = "ID:"
	spec_lbl.custom_minimum_size = Vector2(30, 0)
	id_row.add_child(spec_lbl)

	specimen_id_input = LineEdit.new()
	specimen_id_input.text = "CT-ALPHA-01"
	specimen_id_input.custom_minimum_size = Vector2(120, 0)
	id_row.add_child(specimen_id_input)

	var spectral_row := HBoxContainer.new()
	vbox.add_child(spectral_row)

	var spec_title := Label.new()
	spec_title.text = "Spectral Constant:"
	spec_title.custom_minimum_size = Vector2(140, 0)
	spectral_row.add_child(spec_title)

	spectral_opt = OptionButton.new()
	spectral_opt.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for spec in SPECTRAL_CONSTANTS:
		spectral_opt.add_item(spec["name"])
	spectral_opt.item_selected.connect(_on_spectral_constant_selected)
	spectral_row.add_child(spectral_opt)

	vbox.add_child(HSeparator.new())

	var sub_tabs := TabContainer.new()
	sub_tabs.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vbox.add_child(sub_tabs)

	var osteo_box := VBoxContainer.new()
	osteo_box.name = "Osteology"
	osteo_box.add_theme_constant_override("separation", 6)
	sub_tabs.add_child(osteo_box)
	_add_creator_slider(osteo_box, "Cranial Vault Depth", SomaticEngineScript.ParamIdx.CRANIAL_VAULT_DEPTH, 0.80, 1.30, 1.15)
	_add_creator_slider(osteo_box, "Calvaria Armor Offset", SomaticEngineScript.ParamIdx.CLEARANCE_CRANIAL_CALVARIA_OFFSET, 0.0, 1.0, 0.20)
	_add_creator_slider(osteo_box, "Pelvic Bicristal Width", SomaticEngineScript.ParamIdx.OSTEOLOGY_BICRISTAL_PELVIC_WIDTH, 0.0, 1.0, 0.40)

	var myo_box := VBoxContainer.new()
	myo_box.name = "Myology"
	myo_box.add_theme_constant_override("separation", 6)
	sub_tabs.add_child(myo_box)
	_add_creator_slider(myo_box, "Visceral Adipose", SomaticEngineScript.ParamIdx.ADIPOSE_VISCERAL, 0.0, 1.0, 0.85)
	_add_creator_slider(myo_box, "Femoral Adipose", SomaticEngineScript.ParamIdx.ADIPOSE_FEMORAL_ANTERIOR, 0.0, 1.0, 0.40)
	_add_creator_slider(myo_box, "Pectoral Hypertrophy", SomaticEngineScript.ParamIdx.HYPERTROPHY_PECTORALIS_MAJOR, 0.0, 1.0, 0.90)
	_add_creator_slider(myo_box, "Quadriceps Hypertrophy", SomaticEngineScript.ParamIdx.HYPERTROPHY_RECTUS_FEMORIS, 0.0, 1.0, 0.75)
	_add_creator_slider(myo_box, "Forearm Vascularity", SomaticEngineScript.ParamIdx.VASCULARITY_FOREARM_ANTERIOR, 0.0, 1.0, 0.80)

	var derm_box := VBoxContainer.new()
	derm_box.name = "Dermis"
	derm_box.add_theme_constant_override("separation", 6)
	sub_tabs.add_child(derm_box)
	_add_creator_slider(derm_box, "Basal Erythema", SomaticEngineScript.ParamIdx.DERMAL_ERYTHEMA_BASAL, 0.0, 1.0, 0.60)
	_add_creator_slider(derm_box, "Melanin Tone", SomaticEngineScript.ParamIdx.DERMAL_MELANIN_CONCENTRATION, 0.0, 1.0, 0.45)

	var theo_box := VBoxContainer.new()
	theo_box.name = "Theology"
	theo_box.add_theme_constant_override("separation", 6)
	sub_tabs.add_child(theo_box)
	_add_creator_slider(theo_box, "A-Field Conductance", SomaticEngineScript.ParamIdx.RESONANCE_AFIELD_CONDUCTANCE, 0.0, 2.0, 1.45)
	_add_creator_slider(theo_box, "Ocular Cyan Radiance", SomaticEngineScript.ParamIdx.RESONANCE_OCULAR_CYAN_LUMINOSITY, 0.0, 2.5, 0.92)

	vbox.add_child(HSeparator.new())

	var btn_row := HBoxContainer.new()
	vbox.add_child(btn_row)

	var randomize_btn := Button.new()
	randomize_btn.text = "🎲 Randomize Somatics"
	randomize_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	randomize_btn.pressed.connect(_on_randomize_pressed)
	btn_row.add_child(randomize_btn)

	var save_btn := Button.new()
	save_btn.text = "💾 Save & Bake .DNA"
	save_btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	save_btn.pressed.connect(_on_save_pressed)
	btn_row.add_child(save_btn)

	status_lbl = Label.new()
	status_lbl.text = "Ready to sculpt new specimen."
	status_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	status_lbl.add_theme_color_override("font_color", Color(0.4, 0.9, 0.5))
	vbox.add_child(status_lbl)

func _add_creator_slider(parent: Control, txt: String, idx: int, min_v: float, max_v: float, def_v: float) -> void:
	var row := HBoxContainer.new()
	parent.add_child(row)

	var l := Label.new()
	l.text = txt
	l.custom_minimum_size = Vector2(170, 0)
	row.add_child(l)

	var val_lbl := Label.new()
	val_lbl.text = "%.2f" % def_v
	val_lbl.custom_minimum_size = Vector2(45, 0)

	var s := HSlider.new()
	s.min_value = min_v
	s.max_value = max_v
	s.step = 0.01
	s.value = def_v
	s.custom_minimum_size = Vector2(180, 24)
	s.size_flags_horizontal = Control.SIZE_EXPAND_FILL

	slider_map[idx] = {"slider": s, "label": val_lbl}

	s.value_changed.connect(func(v: float):
		val_lbl.text = "%.2f" % v
		if somatic_engine and somatic_engine.has_method("set_param_by_index"):
			somatic_engine.set_param_by_index(idx, v)
			if somatic_bridge and somatic_bridge.has_method("synchronize_bridge"):
				somatic_bridge.synchronize_bridge()
	)
	row.add_child(s)
	row.add_child(val_lbl)

func _on_spectral_constant_selected(index: int) -> void:
	if index < 0 or index >= SPECTRAL_CONSTANTS.size(): return
	var spec: Dictionary = SPECTRAL_CONSTANTS[index]
	_apply_slider_value(SomaticEngineScript.ParamIdx.ADIPOSE_VISCERAL, spec["visceral_fat"])
	_apply_slider_value(SomaticEngineScript.ParamIdx.HYPERTROPHY_PECTORALIS_MAJOR, spec["pec_hyp"])
	_apply_slider_value(SomaticEngineScript.ParamIdx.CRANIAL_VAULT_DEPTH, spec["cranial_depth"])
	_apply_slider_value(SomaticEngineScript.ParamIdx.DERMAL_ERYTHEMA_BASAL, spec["erythema"])
	_apply_slider_value(SomaticEngineScript.ParamIdx.RESONANCE_AFIELD_CONDUCTANCE, spec["conductance"])
	
	if somatic_bridge:
		somatic_bridge.set("base_afield_potency", spec["base_afield"])
		somatic_bridge.synchronize_bridge()
	status_lbl.text = "Applied template: %s" % spec["name"]

func _apply_slider_value(idx: int, val: float) -> void:
	if slider_map.has(idx):
		var entry: Dictionary = slider_map[idx]
		entry["slider"].value = val
		entry["label"].text = "%.2f" % val
	if somatic_engine and somatic_engine.has_method("set_param_by_index"):
		somatic_engine.set_param_by_index(idx, val)

func _on_randomize_pressed() -> void:
	for idx in slider_map:
		var entry: Dictionary = slider_map[idx]
		var s: HSlider = entry["slider"]
		s.value = randf_range(s.min_value, s.max_value)
	if somatic_bridge and somatic_bridge.has_method("synchronize_bridge"):
		somatic_bridge.synchronize_bridge()
	status_lbl.text = "🎲 Random somatic profile generated."

func _on_save_pressed() -> void:
	var char_name: String = name_input.text.strip_edges()
	var spec_id: String = specimen_id_input.text.strip_edges()
	if char_name.is_empty(): char_name = "Custom_Specimen"
	if spec_id.is_empty(): spec_id = "SPEC-01"

	var spec_idx: int = spectral_opt.selected
	var spec_data: Dictionary = SPECTRAL_CONSTANTS[spec_idx] if spec_idx >= 0 and spec_idx < SPECTRAL_CONSTANTS.size() else SPECTRAL_CONSTANTS[0]

	var slug: String = char_name.to_lower().replace(" ", "_")
	var recipe_path := "res://03_godot_client/archetypes/%s.json" % slug
	var dna_path := "res://03_godot_client/archetypes/%s.dna" % slug

	var raw_arr: PackedFloat32Array
	if somatic_engine: raw_arr = somatic_engine.get("raw_values")

	var recipe := {
		"specimen_id": spec_id, "archetype_name": char_name, "caste": spec_data["caste"],
		"spectral_constant": spec_data["id"], "dialetheic_afield": spec_data["base_afield"],
		"master_texture_path": "res://assets/portraits/master_atlas_strip.png", "anatomical_parameters": {}
	}

	var json_file := FileAccess.open(recipe_path, FileAccess.WRITE)
	if json_file:
		json_file.store_string(JSON.stringify(recipe, "  "))
		json_file.close()

	if somatic_engine:
		var dna_file := FileAccess.open(dna_path, FileAccess.WRITE)
		if dna_file:
			var buf := PackedByteArray()
			buf.resize(512)
			for i in range(128): buf.encode_float(i * 4, raw_arr[i] if i < raw_arr.size() else 0.0)
			dna_file.store_buffer(buf)
			dna_file.close()

	status_lbl.text = "💾 Saved & baked: %s.dna" % slug
	character_saved.emit(spec_id, recipe_path, dna_path)
