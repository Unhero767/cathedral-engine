extends Node
class_name CathedralSceneBootstrap

func _ready() -> void:
    print("[CATHE-BOOTSTRAP] Verifying viewport scene root and spatial manifold...")
    var viewport := get_viewport()
    if not viewport.get_camera_3d():
        var cam := Camera3D.new()
        cam.name = "FallbackCamera3D"
        cam.look_at_from_position(Vector3(0, 5, 10), Vector3.ZERO, Vector3.UP)
        add_child(cam)
        cam.make_current()

    if not get_node_or_null("FallbackLight"):
        var light := DirectionalLight3D.new()
        light.name = "FallbackLight"
        light.rotation_degrees = Vector3(-45, 45, 0)
        light.shadow_enabled = true
        add_child(light)

    var mesh_instance = get_node_or_null("SplatMeshInstance3D")
    if not mesh_instance:
        mesh_instance = MeshInstance3D.new()
        mesh_instance.name = "SplatMeshInstance3D"
        var sphere := SphereMesh.new()
        sphere.radius = 1.0
        sphere.height = 2.0
        mesh_instance.mesh = sphere
        
        var mat := StandardMaterial3D.new()
        mat.albedo_color = Color(0.1, 0.4, 0.9, 1.0) # Blue/Sorrow constant
        mat.emission_enabled = true
        mat.emission = Color(0.1, 0.4, 0.9)
        mat.emission_energy_multiplier = 2.5
        mesh_instance.material_override = mat
        add_child(mesh_instance)
        print("[CATHE-BOOTSTRAP] Blue/Sorrow spatial geometry initialized.")

    # Attach live runtime WebSocket bridge for dynamic strain modulation
    var bridge_script = load("res://scripts/CathedralRuntimeBridge.gd")
    if bridge_script and not get_node_or_null("CathedralRuntimeBridge"):
        var bridge = bridge_script.new()
        bridge.name = "CathedralRuntimeBridge"
        add_child(bridge)
        print("[CATHE-BOOTSTRAP] Live WebSocket telemetry bridge attached.")
