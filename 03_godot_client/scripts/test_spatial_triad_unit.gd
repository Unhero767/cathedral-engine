extends SceneTree

## Headless Unit Test Suite for EAS-03 Spatial Triad Engine
## Run with: /Applications/Godot.app/Contents/MacOS/Godot --headless -s test_spatial_triad_unit.gd

const SpatialTriadController = preload("res://03_godot_client/scripts/spatial_triad_controller.gd")

func _init() -> void:
	print("=================================================================")
	print("[TEST RUNNER] Starting EAS-03 Spatial Triad Test Suite...")
	print("=================================================================")
	
	var all_passed := true
	all_passed = all_passed and test_belnap_dunn_transitions()
	all_passed = all_passed and test_metamorphic_squeeze_cost()
	all_passed = all_passed and test_ash_archive_merkle_integrity()
	all_passed = all_passed and test_afield_horizon_scaling()
	
	print("=================================================================")
	if all_passed:
		print("[TEST SUITE PASSED] All 4 formal verification suites succeeded.")
	else:
		print("[TEST SUITE FAILED] One or more verification suites failed.")
	print("=================================================================")
	quit(0 if all_passed else 1)

func test_belnap_dunn_transitions() -> bool:
	print("[TEST 1] Testing Belnap-Dunn Four-Valued Coordinate Validation...")
	var controller = SpatialTriadController.new()
	
	controller.set_coordinate_truth(Vector2i(0, 0), SpatialTriadController.BelnapDunnValue.T)
	controller.set_coordinate_truth(Vector2i(1, 0), SpatialTriadController.BelnapDunnValue.F)
	controller.set_coordinate_truth(Vector2i(2, 0), SpatialTriadController.BelnapDunnValue.B)
	
	assert(controller._evaluate_spatial_truth(Vector2i(0, 0)) == SpatialTriadController.BelnapDunnValue.T)
	assert(controller._evaluate_spatial_truth(Vector2i(1, 0)) == SpatialTriadController.BelnapDunnValue.F)
	assert(controller._evaluate_spatial_truth(Vector2i(2, 0)) == SpatialTriadController.BelnapDunnValue.B)
	assert(controller._evaluate_spatial_truth(Vector2i(99, 99)) == SpatialTriadController.BelnapDunnValue.N)
	
	controller.free()
	print("[TEST 1 PASSED] Belnap-Dunn state evaluations verified.")
	return true

func test_metamorphic_squeeze_cost() -> bool:
	print("[TEST 2] Testing Metamorphic Squeeze Algorithmic Cost (c <= 0.30)...")
	var controller = SpatialTriadController.new()
	controller.enable_metamorphic_squeeze = true
	controller.ego_density = 8.3
	
	var initial_velocity := Vector2(100.0, 0.0)
	var resolved_velocity: Vector2 = controller._resolve_dialetheic_step(Vector2i(5, 5), initial_velocity, 0.016)
	
	assert(controller._harmonic_scars.size() == 1)
	var scar: Dictionary = controller._harmonic_scars[0]
	assert(scar["algorithmic_cost"] <= 0.30, "Algorithmic cost exceeds TRIZ ceiling")
	assert(scar["structural_load_capacity"] >= (1.0 / 0.30))
	assert(resolved_velocity.length() > 0.0, "Kinetic momentum must be transmitted")
	
	controller.free()
	print("[TEST 2 PASSED] Metamorphic Squeeze verified with cost c=%.2f." % scar["algorithmic_cost"])
	return true

func test_ash_archive_merkle_integrity() -> bool:
	print("[TEST 3] Testing Ash Archive Merkle DAG Ledger & Lex I Never-Overwrite...")
	var controller = SpatialTriadController.new()
	controller._initialize_ash_archive()
	
	controller._commit_telemetry_event("INIT", {"data": 1})
	controller._commit_telemetry_event("TRANSITION", {"step": 2})
	controller._commit_telemetry_event("SCAR", {"cost": 0.28})
	
	assert(controller.get_ash_archive_ledger_count() == 3)
	assert(controller.verify_ash_archive_integrity() == true, "Merkle DAG hash chain validation failed")
	
	controller._ash_archive_ledger[1]["payload"]["step"] = 999
	assert(controller.verify_ash_archive_integrity() == false, "Tampering was not caught")
	
	controller.free()
	print("[TEST 3 PASSED] Ash Archive Merkle DAG cryptographic integrity verified.")
	return true

func test_afield_horizon_scaling() -> bool:
	print("[TEST 4] Testing A-Field Spatial Radius Scaling...")
	var controller = SpatialTriadController.new()
	controller.ego_density = 8.3
	controller._current_emotional_magnitude = 1.0
	controller.afield_beta = 0.42
	
	controller._calculate_afield_kinetics()
	var baseline_r: float = controller._current_afield_radius
	assert(abs(baseline_r - 90.88) < 0.01)
	
	controller.ego_density = 16.6
	controller._current_emotional_magnitude = 2.0
	controller._calculate_afield_kinetics()
	var surge_r: float = controller._current_afield_radius
	assert(abs(surge_r - 171.52) < 0.01)
	
	controller.free()
	print("[TEST 4 PASSED] A-Field horizon scaling formulas verified.")
	return true
