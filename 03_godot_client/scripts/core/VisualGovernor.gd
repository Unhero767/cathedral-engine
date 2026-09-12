extends MeshInstance3D

@export var target_key: String = "TARGET_PRESENT"

func _ready() -> void:
    # Ensure the material is unique to this node so it doesn't affect all meshes globally
    if material_override == null:
        material_override = StandardMaterial3D.new()
    
    # Load and apply our custom harmonic scar shader
    var shader = load("res://shaders/HarmonicScar.gdshader")
    if shader:
        var mat = ShaderMaterial.new()
        mat.shader = shader
        material_override = mat

func _process(_delta: float) -> void:
    # Safely query the engine for the latest event metrics
    var ledger = CathedralEngine.get_ledger_snapshot()
    if ledger.size() > 0:
        var latest_event = ledger[ledger.size() - 1]
        
        # Pass the logical stress metric (Omega L) directly to the shader uniform
        if material_override is ShaderMaterial:
            (material_override as ShaderMaterial).set_shader_parameter("omega_l", latest_event.omega_l)
