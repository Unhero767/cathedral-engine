# File: scripts/master_world_bootstrap.gd
# Bootstraps the full visual environment with WorldEnvironment, HDR Glow, and Volumetric Fog.
extends Node3D

const ClientScript = preload("res://scripts/cathedral_presentation_client.gd")
const HeartOculusShader = preload("res://shaders/HeartOculus.gdshader")

func _ready() -> void:
	print("[MasterWorld] Initializing Cathedral Environment...")

	# 1. WorldEnvironment Configuration
	var env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.02, 0.02, 0.04, 1.0)

	# HDR Additive Glow
	env.glow_enabled = true
	env.glow_intensity = 1.0
	env.glow_bloom = 0.2
	env.glow_hdr_threshold = 1.2
	env.glow_blend_mode = Environment.GLOW_BLEND_MODE_ADDITIVE

	# Volumetric Fog
	env.volumetric_fog_enabled = true
	env.volumetric_fog_density = 0.05
	env.volumetric_fog_albedo = Color(0.10, 0.10, 0.10, 1.0)
	env.volumetric_fog_length = 64.0

	var world_env = WorldEnvironment.new()
	world_env.environment = env
	add_child(world_env)

	# 2. Camera & Directional Lighting
	var camera = Camera3D.new()
	camera.position = Vector3(0.0, 1.2, 3.5)
	camera.look_at(Vector3(0.0, 0.5, 0.0), Vector3.UP)
	add_child(camera)

	var light = DirectionalLight3D.new()
	light.position = Vector3(5.0, 10.0, 5.0)
	light.look_at(Vector3.ZERO, Vector3.UP)
	light.light_energy = 0.8
	add_child(light)

	# 3. HeartOculus MeshInstance3D
	var oculus_mesh = MeshInstance3D.new()
	oculus_mesh.name = "HeartOculus"
	oculus_mesh.mesh = BoxMesh.new()

	var shader_mat = ShaderMaterial.new()
	shader_mat.shader = HeartOculusShader
	oculus_mesh.material_override = shader_mat
	add_child(oculus_mesh)

	# 4. Presentation Client
	var client = ClientScript.new()
	client.name = "ManifoldClient"
	client.target_mesh = oculus_mesh
	client.websocket_url = "ws://127.0.0.1:8765/ws/manifold"
	add_child(client)

	print("[MasterWorld] Environment, Shader, and Presentation Client bound successfully.")
