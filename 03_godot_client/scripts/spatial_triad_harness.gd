class_name SpatialTriadHarness
extends Node2D

## EAS-03 Spatial Triad Interactive Demo Harness & Telemetry HUD
## System Classification: MLAOS-PRIME // ARCHITECTONIC-FIELD-V4
## Prime Isomorphism Axiom: Emotion == Physics == Magic == Biology == Architecture

const SpatialTriadController = preload("res://03_godot_client/scripts/spatial_triad_controller.gd")

@onready var controller: SpatialTriadController = $SpatialTriadController
@onready var hud_label_telemetry: Label = $HUD/MarginContainer/VBoxContainer/TelemetryLabel
@onready var hud_label_ledger: Label = $HUD/MarginContainer/VBoxContainer/LedgerLabel
@onready var hud_label_scars: Label = $HUD/MarginContainer/VBoxContainer/ScarsLabel
@onready var hud_label_help: Label = $HUD/MarginContainer/VBoxContainer/HelpLabel

const GRID_CELL_SIZE: float = 16.0

func _ready() -> void:
	_setup_test_spatial_grid()
	_connect_controller_signals()
	_update_hud_display()

func _setup_test_spatial_grid() -> void:
	if not controller:
		return
		
	# 1. True Chamber (Sound / Open): Grid (0..10, 0..10)
	for x in range(0, 11):
		for y in range(0, 11):
			controller.set_coordinate_truth(Vector2i(x, y), SpatialTriadController.BelnapDunnValue.T)
			
	# 2. Obsidian Ward (False / Blocked): Perimeter walls
	for x in range(-5, 20):
		controller.set_coordinate_truth(Vector2i(x, -5), SpatialTriadController.BelnapDunnValue.F)
		controller.set_coordinate_truth(Vector2i(x, 15), SpatialTriadController.BelnapDunnValue.F)
	for y in range(-5, 16):
		controller.set_coordinate_truth(Vector2i(-5, y), SpatialTriadController.BelnapDunnValue.F)
		controller.set_coordinate_truth(Vector2i(20, y), SpatialTriadController.BelnapDunnValue.F)
		
	# 3. Dialetheic Rupture (Both / Contradiction Gates): Line at x=5
	for y in range(2, 9):
		controller.set_coordinate_truth(Vector2i(5, y), SpatialTriadController.BelnapDunnValue.B)

func _connect_controller_signals() -> void:
	if not controller:
		return
	controller.state_transition_committed.connect(_on_state_transition_committed)
	controller.dialetheic_collision_detected.connect(_on_dialetheic_collision)
	controller.harmonic_scar_petrified.connect(_on_harmonic_scar_petrified)
	controller.afield_kinetics_updated.connect(_on_afield_kinetics_updated)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_SPACE:
				controller.pulse_dialogue_stress(randf_range(0.65, 1.0))
			KEY_1:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.THETA_GOLD
			KEY_2:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.PSI_TEAL
			KEY_3:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.DELTA_BLUE
			KEY_4:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.PHI_RED
			KEY_5:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.OMEGA_VIOLET
			KEY_6:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.EPSILON_EMERALD
			KEY_0:
				controller.active_spectral_constant = SpatialTriadController.SpectralConstant.NULL_OBSIDIAN
			KEY_UP:
				if Input.is_key_pressed(KEY_SHIFT):
					controller.ego_density = min(controller.ego_density + 0.5, 25.0)
			KEY_DOWN:
				if Input.is_key_pressed(KEY_SHIFT):
					controller.ego_density = max(controller.ego_density - 0.5, 1.0)
		_update_hud_display()

func _on_state_transition_committed(_event_record: Dictionary) -> void:
	_update_hud_display()

func _on_dialetheic_collision(coord: Vector2, resolution_type: String) -> void:
	print("[HARNESS] Dialetheic Collision at %s | Resolving via %s" % [coord, resolution_type])

func _on_harmonic_scar_petrified(scar_data: Dictionary) -> void:
	print("[HARNESS] Harmonic Scar Formed at %s | Algorithmic Cost c=%.2f | Load Capacity=%.2f" % [
		scar_data["coordinate"],
		scar_data["algorithmic_cost"],
		scar_data["structural_load_capacity"]
	])
	queue_redraw()
	_update_hud_display()

func _on_afield_kinetics_updated(_radius: float, _velocity: Vector2) -> void:
	_update_hud_display()

func _draw() -> void:
	for scar in controller._harmonic_scars:
		var grid_coord: Array = scar["coordinate"]
		var world_pos := Vector2(grid_coord[0] * GRID_CELL_SIZE, grid_coord[1] * GRID_CELL_SIZE)
		var scar_rect := Rect2(world_pos, Vector2(GRID_CELL_SIZE, GRID_CELL_SIZE))
		draw_rect(scar_rect, Color(1.0, 0.82, 0.28, 0.45), true)
		draw_line(world_pos, world_pos + Vector2(GRID_CELL_SIZE, GRID_CELL_SIZE), Color(1.0, 0.82, 0.28, 0.9), 2.0)
		draw_line(world_pos + Vector2(GRID_CELL_SIZE, 0), world_pos + Vector2(0, GRID_CELL_SIZE), Color(0.0, 0.92, 1.0, 0.9), 2.0)

func _update_hud_display() -> void:
	if not controller or not hud_label_telemetry:
		return
		
	var spectral_names := ["THETA (Gold / Joy)", "PSI (Teal / Curiosity)", "DELTA (Blue / Sorrow)", "PHI (Red / Anger)", "OMEGA (Violet / Fear)", "EPSILON (Emerald / Love)", "NULL (Obsidian / Void)"]
	var active_spec_name: String = spectral_names[controller.active_spectral_constant]
	
	hud_label_telemetry.text = "EAS-03 TELEMETRY // A-FIELD HORIZON\n" + \
		"Position: %s | Velocity: %s\n" % [controller.global_position.round(), controller.velocity.round()] + \
		"Spectral Constant: %s\n" % active_spec_name + \
		"Ego Density (rho): %.2f (Baseline 8.3) | A-Field Radius: %.1f px\n" % [controller.ego_density, controller._current_afield_radius] + \
		"Sub-pixel Remainder: (%.3f, %.3f)" % [controller._subpixel_accumulator.x, controller._subpixel_accumulator.y]
		
	hud_label_ledger.text = "ASH ARCHIVE (LEX I MERKLE LEDGER)\n" + \
		"Blocks Committed: %d | Integrity: %s\n" % [controller.get_ash_archive_ledger_count(), "VERIFIED_VALID" if controller.verify_ash_archive_integrity() else "INTEGRITY_FAULT"] + \
		"Latest J_hash: %s..." % controller._latest_block_hash.substr(0, 16)
		
	hud_label_scars.text = "PARACONSISTENT STATE\n" + \
		"Harmonic Scars Formed: %d | Dialetheic Turbulence: %.2f" % [controller._harmonic_scars.size(), controller._dialetheic_turbulence]
		
	if hud_label_help:
		hud_label_help.text = "CONTROLS: Arrow Keys=Move | Space=Dialogue Cadence Pulse | 1-6,0=Switch Spectral Constant | Shift+Up/Down=Modulate Ego Density"
