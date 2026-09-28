extends Node
class_name CathedralTelemetryPoller

var http_request: HTTPRequest
var telemetry_url: String = "http://localhost:8000/api/v1/telemetry/state"
var hud_label: Label

# Drag your 3D MeshInstance3D here in the Inspector, or leave it to auto-find
@export var cube_mesh: MeshInstance3D

func _ready() -> void:
	var canvas_layer = find_child("CanvasLayer", true, false) as CanvasLayer
	if not canvas_layer:
		canvas_layer = CanvasLayer.new()
		add_child(canvas_layer)
	
	hud_label = find_child("Label", true, true) as Label
	if not hud_label:
		hud_label = Label.new()
		hud_label.position = Vector2(40, 40)
		hud_label.add_theme_font_size_override("font_size", 24)
		canvas_layer.add_child(hud_label)

	if not cube_mesh:
		cube_mesh = get_node_or_null("../MeshInstance3D") as MeshInstance3D

	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)
	
	var timer = Timer.new()
	timer.wait_time = 1.0
	timer.autostart = true
	timer.timeout.connect(_poll_server)
	add_child(timer)

func _poll_server() -> void:
	http_request.request(telemetry_url)

func _on_request_completed(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.new()
		if json.parse(body.get_string_from_utf8()) == OK:
			var data = json.get_data() as Dictionary
			if data.has("z_active") and data.has("merkle_hash"):
				var z_val = data["z_active"] as float
				var merkle = data["merkle_hash"] as String
				
				# Update HUD overlay text
				if hud_label:
					hud_label.text = "Z: %.1f | Hash: %s" % [z_val, merkle]
				
				# Push telemetry variable into the 3D Shader uniform
				if cube_mesh:
					var mat = cube_mesh.get_active_material(0) as ShaderMaterial
					if mat:
						mat.set_shader_parameter("z_active", z_val)
						
				print("[TelemetryPoller] Synchronized Z-active: ", z_val)
