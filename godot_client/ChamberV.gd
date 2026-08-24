#==============================================================================
# ChamberV.gd - Godot 4.x Spatial Tilemap & Node Ingestion Manager
# Ingests dynamic 8x8 grid coordinates and auto-spawns Portals, Pillars, Altar, Oculus
#==============================================================================
extends Node2D

@export var tile_size: Vector2 = Vector2(64, 64)
@export var grid_origin: Vector2 = Vector2(80, 80)

@onready var sync_bridge: Node = get_node_or_null("/root/CathedralSync")
@onready var grid_container: Node2D = get_node_or_null("SpatialGridContainer")
@onready var state_label: Label = get_node_or_null("HUDLayer/TelemetryPanel/StateLabel")
@onready var oracle_log: RichTextLabel = get_node_or_null("HUDLayer/TelemetryPanel/OracleCardLog")
@onready var draw_button: Button = get_node_or_null("HUDLayer/TelemetryPanel/DrawOracleButton")
@onready var resonance_rect: ColorRect = get_node_or_null("ShaderOverlayLayer/ResonanceScreenRect")

var spectral_colors: Dictionary = {
	"GOLD": Color("#E5C07B"),
	"TEAL": Color("#4EC9B0"),
	"BLUE": Color("#569CD6"),
	"RED": Color("#E06C75"),
	"VIOLET": Color("#C678DD"),
	"EMERALD": Color("#98C379"),
	"NULL": Color("#1E1E1E")
}

func _ready() -> void:
	if grid_container == null:
		grid_container = Node2D.new()
		grid_container.position = grid_origin
		add_child(grid_container)

	if draw_button:
		draw_button.pressed.connect(_on_draw_button_pressed)

	if sync_bridge:
		sync_bridge.state_updated.connect(_on_state_updated)
		sync_bridge.chamber_loaded.connect(_on_chamber_loaded)
		sync_bridge.flux_updated.connect(_on_flux_updated)
		sync_bridge.card_drawn.connect(_on_card_drawn)
		sync_bridge.fetch_chamber(5)
		sync_bridge.fetch_rpg_state()
	else:
		print("[ChamberV] Running in standalone demo mode.")
		_generate_mock_chamber_v()

func _on_draw_button_pressed() -> void:
	if sync_bridge:
		sync_bridge.draw_oracle_card("Gold-Obsidian", "T")

func _on_state_updated(data: Dictionary) -> void:
	if state_label:
		state_label.text = "Turn: %d | Era: %s\nPolitical Tension (τ): %.2f\nResource Scarcity (ρ): %.2f\nFaction Drift (δ): %.2f\nSystemic Coherence (σ): %.2f\nCarrier Frequency: %.2f Hz\nA-Field Flux (dΦ/dt): %.3f rad/s\nSpectral Dominant: [%s]" % [
			data.get("turn", 1),
			data.get("era_name", "Era of Kinetic Remaking"),
			data.get("tau_pol", 0.44),
			data.get("rho_res", 0.38),
			data.get("delta_fac", 0.35),
			data.get("sigma_coh", 0.72),
			data.get("carrier_hz", 130.81),
			data.get("flux_dphi_dt", 0.428),
			data.get("active_spectral", "RED")
		]

func _on_card_drawn(result: Dictionary) -> void:
	if oracle_log:
		var card = result.get("card", {})
		var belnap = result.get("belnap_resolution", {})
		var spec = card.get("spectral", "GOLD")
		var itype = result.get("interference_type", "Constructive")
		var i_val = result.get("interference_intensity", 1.0)
		
		var log_text = "[b]ORACLE CARD DRAWN:[/b] [color=%s]#%d - %s[/color]\n" % [
			spectral_colors.get(spec, Color.WHITE).to_html(),
			card.get("card_id", 0),
			card.get("name", "Unknown Card")
		]
		log_text += "[b]Arcana:[/b] %s\n" % [card.get("arcana", "")]
		log_text += "[b]Lore:[/b] [i]%s[/i]\n" % [card.get("flavour_lore", "")]
		log_text += "[b]Wave Interference:[/b] %s (Intensity: %.2f)\n" % [itype, i_val]
		log_text += "[b]Belnap Resolution:[/b] %s (Cost: %.2f)\n" % [
			belnap.get("truth_value", "T"),
			belnap.get("algorithmic_cost", 0.05)
		]
		if belnap.get("harmonic_scar_formed", false):
			log_text += "[color=#E5C07B][b]★ Harmonic Scar Petrified into Basalt Pillar[/b][/color]\n"
		oracle_log.text = log_text

func _on_chamber_loaded(chamber_data: Dictionary) -> void:
	_clear_grid()
	var nodes_list: Array = chamber_data.get("nodes", [])
	for node_dict in nodes_list:
		_spawn_chamber_node(node_dict)

func _spawn_chamber_node(data: Dictionary) -> void:
	var x: int = data.get("x", 0)
	var y: int = data.get("y", 0)
	var node_type: String = data.get("node_type", "floor")
	var node_id: String = data.get("node_id", "")
	var spectral_str: String = data.get("spectral", "TEAL")
	var metadata: Dictionary = data.get("metadata", {})

	var world_pos = Vector2(x * tile_size.x, y * tile_size.y)
	var node_instance: Node2D

	match node_type:
		"portal":
			node_instance = _create_portal_node(node_id, spectral_str, metadata)
		"pillar":
			node_instance = _create_pillar_node(node_id, spectral_str, metadata)
		"altar":
			node_instance = _create_altar_node(node_id, metadata)
		"oculus":
			node_instance = _create_oculus_node(node_id, metadata)
		"wall":
			node_instance = _create_wall_node(node_id, metadata)
		_:
			node_instance = _create_floor_node(node_id, spectral_str, metadata)

	node_instance.position = world_pos
	node_instance.name = node_id
	grid_container.add_child(node_instance)

func _create_portal_node(id: String, spec: String, meta: Dictionary) -> Node2D:
	var root = Node2D.new()
	var rect = ColorRect.new()
	rect.size = tile_size
	rect.color = spectral_colors.get(spec, Color.CYAN)
	root.add_child(rect)

	var label = Label.new()
	label.text = "PORTAL\n" + spec
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.size = tile_size
	root.add_child(label)
	return root

func _create_pillar_node(id: String, spec: String, meta: Dictionary) -> Node2D:
	var root = Node2D.new()
	var rect = ColorRect.new()
	rect.size = tile_size
	rect.color = Color("#2D3748")
	root.add_child(rect)

	var x_label = Label.new()
	x_label.text = "✖ SCAR\nCost: " + str(meta.get("triz_cost", "0.28"))
	x_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	x_label.size = tile_size
	root.add_child(x_label)
	return root

func _create_altar_node(id: String, meta: Dictionary) -> Node2D:
	var root = Node2D.new()
	var rect = ColorRect.new()
	rect.size = tile_size
	rect.color = Color("#C53030")
	root.add_child(rect)

	var label = Label.new()
	label.text = "ATHANOR\n2500°F"
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.size = tile_size
	root.add_child(label)
	return root

func _create_oculus_node(id: String, meta: Dictionary) -> Node2D:
	var root = Node2D.new()
	var rect = ColorRect.new()
	rect.size = tile_size
	rect.color = Color("#D69E2E")
	root.add_child(rect)

	var label = Label.new()
	label.text = "OCULUS\n36-Rings"
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.size = tile_size
	root.add_child(label)
	return root

func _create_wall_node(id: String, meta: Dictionary) -> Node2D:
	var root = Node2D.new()
	var rect = ColorRect.new()
	rect.size = tile_size
	rect.color = Color("#1A202C")
	root.add_child(rect)
	return root

func _create_floor_node(id: String, spec: String, meta: Dictionary) -> Node2D:
	var root = Node2D.new()
	var rect = ColorRect.new()
	rect.size = tile_size
	rect.color = Color("#171923")
	root.add_child(rect)
	return root

func _clear_grid() -> void:
	for child in grid_container.get_children():
		child.queue_free()

func _on_flux_updated(carrier: float, dphi: float) -> void:
	if resonance_rect and resonance_rect.material is ShaderMaterial:
		var mat = resonance_rect.material as ShaderMaterial
		mat.set_shader_parameter("carrier_hz", carrier)
		mat.set_shader_parameter("flux_dphi_dt", dphi)

func _generate_mock_chamber_v() -> void:
	pass
