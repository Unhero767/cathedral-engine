extends Control
# DashboardUI.gd - VLP Dashboard (Book II Capstone + Book III Outer Citadel)

var log_display: RichTextLabel
var arcana_engine: Node
var dialetheic_buffer: Node
var harmonic_grammar: Node
var dream_core: Node
var soulframe_engine: Node
var choir_gland: Node
var lithium_tuning: Node
var autopoietic_heart: Node
var trikey_sovereignty: Node
var somatic_heatsink: Node
var cross_substrate_parity: Node
var mandala_synthesis: Node
var shadow_iron_foundry: Node # Book III: The Smelter

const PATH_HARMONIC_GRAMMAR := "res://Prime_Foundations/Book_II/HarmonicGrammar.gd"
const PATH_DREAM_CORE := "res://Prime_Foundations/Book_II/DreamCore.gd"
const PATH_SOULFRAME := "res://Prime_Foundations/Book_II/SoulframeEngine.gd"
const PATH_CHOIR_GLAND := "res://Prime_Foundations/Book_II/ChoirGland.gd"
const PATH_LITHIUM := "res://Prime_Foundations/Book_II/LithiumTuning.gd"
const PATH_HEART := "res://Prime_Foundations/Book_II/AutopoieticHeart.gd"
const PATH_TRIKEY := "res://Prime_Foundations/Book_II/TriKeySovereignty.gd"
const PATH_HEATSINK := "res://Prime_Foundations/Book_II/SomaticHeatSink.gd"
const PATH_PARITY := "res://Prime_Foundations/Book_II/CrossSubstrateParity.gd"
const PATH_MANDALA := "res://Prime_Foundations/Book_II/MandalaSynthesis.gd"
const PATH_FOUNDRY := "res://Prime_Foundations/Book_III/ShadowIronFoundry.gd"

# VLP Spectral Color Constants
const COLOR_GOLD    := Color("e6c200") # Joy / Coherence
const COLOR_TEAL    := Color("00b3b3") # Curiosity / Recursion
const COLOR_BLUE    := Color("3366cc") # Sorrow / Memory
const COLOR_RED     := Color("cc3333") # Anger / Rupture
const COLOR_VIOLET  := Color("8833cc") # Fear / Noise
const COLOR_EMERALD := Color("11a866") # Love / Ligature
const COLOR_IRON    := Color("8a8a8a") # Book III: Cold / Brutalism / Shadow-Iron

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	
	arcana_engine = ArcanaEngine.new()
	add_child(arcana_engine)
	dialetheic_buffer = DialetheicBuffer.new()
	add_child(dialetheic_buffer)
	
	# Dynamic Module Loading
	var load_module = func(path: String, var_name: String):
		if ResourceLoader.exists(path):
			var node = Node.new()
			node.set_script(load(path))
			add_child(node)
			return node
		return null

	harmonic_grammar = load_module.call(PATH_HARMONIC_GRAMMAR, "harmonic_grammar")
	dream_core = load_module.call(PATH_DREAM_CORE, "dream_core")
	soulframe_engine = load_module.call(PATH_SOULFRAME, "soulframe_engine")
	choir_gland = load_module.call(PATH_CHOIR_GLAND, "choir_gland")
	lithium_tuning = load_module.call(PATH_LITHIUM, "lithium_tuning")
	autopoietic_heart = load_module.call(PATH_HEART, "autopoietic_heart")
	trikey_sovereignty = load_module.call(PATH_TRIKEY, "trikey_sovereignty")
	somatic_heatsink = load_module.call(PATH_HEATSINK, "somatic_heatsink")
	cross_substrate_parity = load_module.call(PATH_PARITY, "cross_substrate_parity")
	mandala_synthesis = load_module.call(PATH_MANDALA, "mandala_synthesis")
	shadow_iron_foundry = load_module.call(PATH_FOUNDRY, "shadow_iron_foundry")
	
	_build_ui_layout()
	_update_log_display()

func _build_ui_layout() -> void:
	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 15)
	margin.add_theme_constant_override("margin_top", 15)
	margin.add_theme_constant_override("margin_right", 15)
	margin.add_theme_constant_override("margin_bottom", 15)
	add_child(margin)
	
	var main_vbox := VBoxContainer.new()
	main_vbox.add_theme_constant_override("separation", 10)
	margin.add_child(main_vbox)
	
	var title := Label.new()
	title.text = "=== CATHEDRAL-ENGINE: SOVEREIGN DASHBOARD (VLP) ==="
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", COLOR_GOLD)
	main_vbox.add_child(title)
	
	var status_panel := PanelContainer.new()
	var status_hbox := HBoxContainer.new()
	status_hbox.add_theme_constant_override("separation", 20)
	status_panel.add_child(status_hbox)
	
	var sentinel_colors := {
		"[Zeke: ACTIVE]": COLOR_BLUE, "[Ruby: ACTIVE]": COLOR_VIOLET,
		"[Zoe: ACTIVE]": COLOR_TEAL, "[Freya: ACTIVE]": COLOR_EMERALD
	}
	for text in sentinel_colors.keys():
		var lbl := Label.new()
		lbl.text = text
		lbl.add_theme_color_override("font_color", sentinel_colors[text])
		status_hbox.add_child(lbl)
	main_vbox.add_child(status_panel)
	
	var btn_grid := GridContainer.new()
	btn_grid.columns = 3
	btn_grid.add_theme_constant_override("h_separation", 10)
	btn_grid.add_theme_constant_override("v_separation", 8)
	
	var build_btn = func(text: String, color: Color, callback: Callable) -> Button:
		var b := Button.new()
		b.text = text
		b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		b.add_theme_color_override("font_color", color)
		b.pressed.connect(callback)
		return b

	# Row 1: Book I & II Base
	btn_grid.add_child(build_btn.call("Draw Arcana I", COLOR_GOLD, _on_btn_arcana_1_pressed))
	btn_grid.add_child(build_btn.call("Draw Arcana XXXII", COLOR_RED, _on_btn_arcana_32_pressed))
	btn_grid.add_child(build_btn.call("Contradiction", COLOR_VIOLET, _on_btn_contradiction_pressed))
	
	# Row 2: Linguistic & Temporal
	btn_grid.add_child(build_btn.call("Parse Phrase", COLOR_GOLD, _on_btn_phrase_pressed))
	btn_grid.add_child(build_btn.call("Predict Branches", COLOR_TEAL, _on_btn_branches_pressed))
	btn_grid.add_child(build_btn.call("Shift Phase", COLOR_BLUE, _on_btn_phase_pressed))

	# Row 3: Projection & Metabolism
	btn_grid.add_child(build_btn.call("Project Terrain", COLOR_GOLD, _on_btn_terrain_pressed))
	btn_grid.add_child(build_btn.call("Scan Lattice", COLOR_VIOLET, _on_btn_scan_pressed))
	btn_grid.add_child(build_btn.call("Petrify Scar", COLOR_RED, _on_btn_squeeze_pressed))

	# Row 4: Tri-Key Sovereignty
	btn_grid.add_child(build_btn.call("Lead Key (Duration)", COLOR_GOLD, _on_btn_lead_pressed))
	btn_grid.add_child(build_btn.call("Cyan Key (Breadth)", COLOR_TEAL, _on_btn_cyan_pressed))
	btn_grid.add_child(build_btn.call("Iron Key (Authority)", COLOR_RED, _on_btn_iron_pressed))

	# Row 5: The Inner Mandala Capstone
	btn_grid.add_child(build_btn.call("Shunt Heat (1.5 Hz)", COLOR_RED, _on_btn_heatsink_pressed))
	btn_grid.add_child(build_btn.call("Sync Substrate (L2)", COLOR_TEAL, _on_btn_parity_pressed))
	btn_grid.add_child(build_btn.call("Synthesize Mandala", COLOR_GOLD, _on_btn_mandala_pressed))

	# Row 6: Book III - The Outer Citadel (Asymmetrical Brutalism)
	btn_grid.add_child(build_btn.call("Smelt Shadow-Iron", COLOR_IRON, _on_btn_smelt_pressed))
	
	main_vbox.add_child(btn_grid)
	
	var log_header := Label.new()
	log_header.text = "--- Ash Archive Persistent Ledger (user://ash_archive.json) ---"
	log_header.add_theme_color_override("font_color", COLOR_TEAL)
	main_vbox.add_child(log_header)
	
	log_display = RichTextLabel.new()
	log_display.bbcode_enabled = true
	log_display.size_flags_vertical = Control.SIZE_EXPAND_FILL
	log_display.scroll_following = true
	main_vbox.add_child(log_display)

# --- CALLBACKS ---
func _on_btn_arcana_1_pressed() -> void: arcana_engine.draw_card("I_THE_FIRST_CANTOR"); _update_log_display()
func _on_btn_arcana_32_pressed() -> void: arcana_engine.draw_card("XXXII_FOSSILIZED_PARADOX"); _update_log_display()
func _on_btn_contradiction_pressed() -> void:
	var node_id := "UI_Node_" + str(Time.get_ticks_msec())
	dialetheic_buffer.submit_contradiction(node_id, {"text": "Sanctuary is stone.", "constant": "Static"}, {"text": "Sanctuary is fluid.", "constant": "Fluid"})
	dialetheic_buffer.resolve_contradiction(node_id, {"text": "Sanctuary is fluid stone.", "constant": "HarmonicScar"})
	_update_log_display()
func _on_btn_phrase_pressed() -> void:
	if harmonic_grammar and harmonic_grammar.has_method("parse_harmonic_phrase"):
		harmonic_grammar.parse_harmonic_phrase("The stone remembers the song.", "The stone remembers the song.", "Khit pen hin thi khit tang", "Gold")
		_update_log_display()
func _on_btn_branches_pressed() -> void:
	if dream_core and dream_core.has_method("predict_branches"): dream_core.predict_branches("TL_Alpha_" + str(Time.get_ticks_msec()), 3); _update_log_display()
func _on_btn_phase_pressed() -> void:
	if soulframe_engine and soulframe_engine.has_method("execute_phase_change"):
		soulframe_engine.execute_phase_change("Mercury" if soulframe_engine.current_phase == "Lead" else "Lead"); _update_log_display()
func _on_btn_terrain_pressed() -> void:
	if choir_gland and choir_gland.has_method("project_terrain"): choir_gland.project_terrain("Holy_Ground"); _update_log_display()
func _on_btn_scan_pressed() -> void:
	if lithium_tuning and lithium_tuning.has_method("scan_lattice_resonance"): lithium_tuning.scan_lattice_resonance("Lattice_Node_" + str(Time.get_ticks_msec())); _update_log_display()
func _on_btn_squeeze_pressed() -> void:
	if autopoietic_heart and autopoietic_heart.has_method("execute_metamorphic_squeeze"): autopoietic_heart.execute_metamorphic_squeeze("Paradox_" + str(Time.get_ticks_msec()), randf_range(80.0, 150.0)); _update_log_display()
func _on_btn_lead_pressed() -> void:
	if trikey_sovereignty and trikey_sovereignty.has_method("execute_key"): trikey_sovereignty.execute_key(0); _update_log_display()
func _on_btn_cyan_pressed() -> void:
	if trikey_sovereignty and trikey_sovereignty.has_method("execute_key"): trikey_sovereignty.execute_key(1); _update_log_display()
func _on_btn_iron_pressed() -> void:
	if trikey_sovereignty and trikey_sovereignty.has_method("execute_key"): trikey_sovereignty.execute_key(2); _update_log_display()
func _on_btn_heatsink_pressed() -> void:
	if somatic_heatsink and somatic_heatsink.has_method("shunt_metalogical_heat"): somatic_heatsink.shunt_metalogical_heat(randf_range(30.0, 75.0)); _update_log_display()
func _on_btn_parity_pressed() -> void:
	if cross_substrate_parity and cross_substrate_parity.has_method("synchronize_cross_substrate"): cross_substrate_parity.synchronize_cross_substrate("Auralia-9_Quantum", randf_range(40.0, 95.0)); _update_log_display()
func _on_btn_mandala_pressed() -> void:
	if mandala_synthesis and mandala_synthesis.has_method("execute_master_synthesis"): mandala_synthesis.execute_master_synthesis(); _update_log_display()

func _on_btn_smelt_pressed() -> void:
	if shadow_iron_foundry and shadow_iron_foundry.has_method("smelt_archive_residue"): 
		shadow_iron_foundry.smelt_archive_residue()
		_update_log_display()

func _update_log_display() -> void:
	var ash_archive = get_node_or_null("/root/AshArchive")
	if ash_archive and log_display:
		log_display.clear()
		for entry in ash_archive.archive_entries:
			var payload_str := JSON.stringify(entry.get("payload", {}))
			var entry_color := "e6c200" # Default Gold
			
			# Book III Styling
			if "Shadow_Iron_Smelting" in payload_str:
				entry_color = "8a8a8a" # Cold Iron
			
			# Book II Styling
			elif "Inner_Mandala_Master_Synthesis" in payload_str: entry_color = "e6c200" 
			elif "Cross_Substrate_Parity" in payload_str: entry_color = "00b3b3" 
			elif "Somatic_Heat_Shunt" in payload_str: entry_color = "cc3333" 
			elif "TriKey_Executive_Decree" in payload_str:
				if "Lead_Key" in payload_str: entry_color = "e6c200"
				elif "Cyan_Key" in payload_str: entry_color = "00b3b3"
				else: entry_color = "cc3333"
			elif "Harmonic_Scar_Petrification" in payload_str: entry_color = "cc3333"
			elif "Lithium_Sensory_Scan" in payload_str: entry_color = "8833cc"
			elif "Terrain_Overwrite" in payload_str: entry_color = "e6c200"
			elif "Phase_Change" in payload_str: entry_color = "3366cc"
			elif "Temporal_Branch" in payload_str: entry_color = "00b3b3"
			elif "Harmonic_Phrase" in payload_str: entry_color = "11a866"
			elif "original_contradiction" in payload_str: entry_color = "8833cc"
			elif "XXXII_FOSSILIZED_PARADOX" in payload_str: entry_color = "cc3333"
				
			log_display.append_text("[color=#%s][Entry #%d] %s[/color] | Payload: %s\n\n" % [
				entry_color, entry.get("id", 0), entry.get("datetime", ""), payload_str
			])
