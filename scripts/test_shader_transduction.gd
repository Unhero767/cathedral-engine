# File: scripts/test_shader_transduction.gd
# Verifies that CathedralPresentationClient updates ShaderMaterial parameters on receipt.
extends SceneTree

const ClientScript = preload("res://scripts/cathedral_presentation_client.gd")
const HeartOculusShader = preload("res://shaders/HeartOculus.gdshader")

var client: Node = null
var mesh_instance: MeshInstance3D = null
var mat: ShaderMaterial = null

func _init() -> void:
	print("[Godot Test] Initializing Shader Transduction Test...")
	
	mesh_instance = MeshInstance3D.new()
	mesh_instance.mesh = BoxMesh.new()
	
	mat = ShaderMaterial.new()
	mat.shader = HeartOculusShader
	mesh_instance.material_override = mat
	root.add_child(mesh_instance)

	client = ClientScript.new()
	client.target_mesh = mesh_instance
	root.add_child(client)

	# Verify Initial Baseline Shader Parameters
	var init_fog = mat.get_shader_parameter("belnap_fog_level")
	var init_entropy = mat.get_shader_parameter("kenomic_entropy")
	print("[Godot Test] Baseline Shader State -> Fog: %s | Entropy: %s" % [str(init_fog), str(init_entropy)])

	# Simulate Incoming Harmonic Scar PCO projection
	var mock_scar_pco = {
		"provenance": {"context": "Spire.Resonance", "tick": 201},
		"epistemic_register": "S",
		"value": {"strain": 0.85},
		"uncertainty_metadata": {
			"belnap_state": "B",
			"is_harmonic_scar": true,
			"kenomic_entropy": 75.0
		}
	}

	print("[Godot Test] Ingesting Mock Harmonic Scar PCO...")
	client._handle_projection_snapshot(JSON.stringify(mock_scar_pco))

	# Verify Transduction Results
	var post_fog = mat.get_shader_parameter("belnap_fog_level")
	var post_entropy = mat.get_shader_parameter("kenomic_entropy")
	var post_emission = mat.get_shader_parameter("u_emission_multiplier")
	var post_strain_gain = mat.get_shader_parameter("u_strain_glow_gain")

	print("[Godot Test] Post-Ingest Shader State -> Fog: %s | Entropy: %s | EmissionMult: %s | GlowGain: %s" % [
		str(post_fog), str(post_entropy), str(post_emission), str(post_strain_gain)
	])

	assert(post_fog == 2, "Transduction Error: belnap_fog_level should be 2 for Harmonic Scar.")
	assert(post_entropy == 75.0, "Transduction Error: kenomic_entropy should be 75.0.")
	assert(post_emission != null and is_equal_approx(float(post_emission), 8.5), "Transduction Error: u_emission_multiplier should be 8.5 for Scar.")
	assert(post_strain_gain != null and is_equal_approx(float(post_strain_gain), 2.125), "Transduction Error: u_strain_glow_gain should be 0.85 * 2.5 = 2.125.")

	print("[Godot Test] Transduction Verified: Shader uniforms match canonical state.")
	quit(0)
