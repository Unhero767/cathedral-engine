# File: scripts/cathedral_scene_bootstrap.gd
# Instances a complete headless/visual test rig with camera, light, mesh, and client.
extends Node3D
class_name CathedralSceneBootstrap

const ClientScript = preload("res://scripts/cathedral_presentation_client.gd")
const DitherShader = preload("res://shaders/SpatialLumenDither.gdshader")

func _ready() -> void:
	# 1. Environment & Lighting
	var light = DirectionalLight3D.new()
	light.position = Vector3(5, 10, 5)
	light.look_at(Vector3.ZERO, Vector3.UP)
	add_child(light)

	# 2. Camera
	var camera = Camera3D.new()
	camera.position = Vector3(0, 0, 4)
	add_child(camera)

	# 3. Target HeartOculus / Mesh Instance
	var mesh_inst = MeshInstance3D.new()
	mesh_inst.name = "HeartOculusMesh"
	mesh_inst.mesh = BoxMesh.new()

	var mat = ShaderMaterial.new()
	mat.shader = DitherShader
	mesh_inst.material_override = mat
	add_child(mesh_inst)

	# 4. Presentation Client
	var client = ClientScript.new()
	client.name = "ManifoldClient"
	client.target_mesh = mesh_inst
	client.websocket_url = "ws://127.0.0.1:8765/ws/manifold"
	add_child(client)

	print("[SceneBootstrap] Viewport pipeline initialized and listening on ws://127.0.0.1:8765/ws/manifold.")
