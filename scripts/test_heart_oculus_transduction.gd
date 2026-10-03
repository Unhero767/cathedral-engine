# File: scripts/test_heart_oculus_transduction.gd
# Verifies that CathedralPresentationClient updates HeartOculus uniforms accurately.
extends SceneTree

const ClientScript = preload("res://scripts/cathedral_presentation_client.gd")
const HeartOculusShader = preload("res://shaders/HeartOculus.gdshader")

var client: Node = null
var oculus_mesh: MeshInstance3D = null
var mat: ShaderMaterial = null

func _init() -> void:
	print("[Godot Test] Initializing HeartOculus Transduction Test...")
	
	oculus_mesh = MeshInstance3D.new()
	oculus_mesh.mesh = BoxMesh.new()
	
	mat = ShaderMaterial.new()
	mat.shader = HeartOculusShader
	oculus_mesh.material_override = mat
	root.add_child(oculus_mesh)

	client = ClientScript.new()
	client.target_mesh = oculus_mesh
	root.add_child(client)

	# Simulate Incoming Harmonic Scar PCO on Spire.Resonance (Gold Joy)
	var mock_scar_pco = {
		"provenance": {"context": "Spire.Resonance", "tick": 401},
		"epistemic_register": "S",
		"value": {"strain": 0.85},
		"uncertainty_metadata": {
			"belnap_state": "B",
			"is_harmonic_scar": true,
			"kenomic_entropy": 75.0
		}
	}

	print("[Godot Test] Ingesting Mock Harmonic Scar PCO for HeartOculus...")
	client._handle_projection_snapshot(JSON.stringify(mock_scar_pco))

	# Verify Transduction Results
	var post_fog = mat.get_shader_parameter("belnap_fog_level")
	var post_entropy = mat.get_shader_parameter("kenomic_entropy")
	var post_mult = mat.get_shader_parameter("u_emission_multiplier")
	var post_glow = mat.get_shader_parameter("u_strain_glow_gain")
	var post_albedo = mat.get_shader_parameter("u_albedo")

	print("[Godot Test] HeartOculus State -> Fog: %s | Entropy: %s | Multiplier: %s | GlowGain: %s | Color: %s" % [
		str(post_fog), str(post_entropy), str(post_mult), str(post_glow), str(post_albedo)
	])

	assert(post_fog == 2, "Transduction Error: belnap_fog_level should be 2.")
	assert(post_entropy == 75.0, "Transduction Error: kenomic_entropy should be 75.0.")
	assert(is_equal_approx(post_mult, 8.5), "Transduction Error: u_emission_multiplier should be 8.5 for Scar.")
	assert(is_equal_approx(post_glow, 2.125), "Transduction Error: u_strain_glow_gain should be 0.85 * 2.5 = 2.125.")

	print("[Godot Test] HeartOculus Transduction Verified: All uniforms match canonical state.")
	quit(0)
