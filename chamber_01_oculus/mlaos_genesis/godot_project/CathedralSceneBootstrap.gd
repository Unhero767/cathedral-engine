@tool
class_name CathedralSceneBootstrap
extends Node3D

@export var auto_spawn_camera: bool = true
@export var auto_spawn_lighting: bool = true
@export var auto_spawn_environment: bool = true
@export var auto_spawn_test_mesh: bool = true

func _ready() -> void:
    if Engine.is_editor_hint():
        return
        
    print("[CathedralSceneBootstrap]: Initializing environment and rendering safety net...")
    
    # 1. Ensure an active Camera3D exists
    if auto_spawn_camera and not get_viewport().get_camera_3d():
        var cam = Camera3D.new()
        cam.name = "SafetyCamera3D"
        cam.current = true
        cam.position = Vector3(0, 1.5, 4)
        cam.look_at(Vector3.ZERO, Vector3.UP)
        add_child(cam)
        print("[CathedralSceneBootstrap]: Spawned safety Camera3D at (0, 1.5, 4).")

    # 2. Ensure lighting exists
    if auto_spawn_lighting:
        var has_light = false
        for child in get_children():
            if child is DirectionalLight3D or child is OmniLight3D or child is SpotLight3D:
                has_light = true
                break
        if not has_light:
            var light = DirectionalLight3D.new()
            light.name = "SafetyDirectionalLight"
            light.light_color = Color(1.0, 0.95, 0.9)
            light.light_energy = 2.0
            light.rotation_degrees = Vector3(-45, 45, 0)
            add_child(light)
            print("[CathedralSceneBootstrap]: Spawned safety DirectionalLight3D.")

    # 3. Ensure WorldEnvironment exists
    if auto_spawn_environment:
        var has_env = false
        for child in get_children():
            if child is WorldEnvironment:
                has_env = true
                break
        if not has_env:
            var we = WorldEnvironment.new()
            we.name = "SafetyWorldEnvironment"
            var env = Environment.new()
            env.background_mode = Environment.BG_COLOR
            env.bg_color = Color(0.05, 0.05, 0.08)
            env.ambient_light_source = Environment.AMBIENT_LIGHT_SOURCE_COLOR
            env.ambient_light_color = Color(0.3, 0.3, 0.35)
            we.environment = env
            add_child(we)
            print("[CathedralSceneBootstrap]: Spawned safety WorldEnvironment.")

    # 4. Ensure a visible test MeshInstance3D exists if none present
    if auto_spawn_test_mesh:
        var has_mesh = false
        for child in get_children():
            if child is MeshInstance3D:
                has_mesh = true
                break
        if not has_mesh:
            var mi = MeshInstance3D.new()
            mi.name = "SafetyTestSphere"
            var sphere = SphereMesh.new()
            sphere.radius = 1.0
            sphere.height = 2.0
            mi.mesh = sphere
            
            var mat = StandardMaterial3D.new()
            mat.albedo_color = Color(0.8, 0.2, 0.1) # Gold/Red cathedral tone
            mat.emission_enabled = true
            mat.emission = Color(0.9, 0.4, 0.1)
            mat.emission_energy_multiplier = 1.5
            mi.material_override = mat
            
            add_child(mi)
            print("[CathedralSceneBootstrap]: Spawned safety MeshInstance3D sphere.")
